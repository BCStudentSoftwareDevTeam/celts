from flask import request, render_template, url_for, g, redirect
from flask import flash, abort, jsonify, session, send_file
from peewee import DoesNotExist, fn, IntegrityError
from playhouse.shortcuts import model_to_dict
import json
from datetime import datetime
import os

from app import app
from app.models.program import Program
from app.models.event import Event
from app.models.user import User
from app.models.eventTemplate import EventTemplate
from app.models.adminLog import AdminLog
from app.models.eventRsvpLog import EventRsvpLog
from app.models.attachmentUpload import AttachmentUpload
from app.models.bonnerCohort import BonnerCohort
from app.models.certification import Certification
from app.models.user import User
from app.models.term import Term
from app.models.eventViews import EventView
from app.models.courseStatus import CourseStatus

from app.logic.userManagement import getAllowedPrograms, getAllowedTemplates
from app.logic.createLogs import createAdminLog
from app.logic.certification import getCertRequirements, updateCertRequirements
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest, getRedirectTarget, setRedirectTarget
from app.logic.events import cancelEvent, deleteEvent, attemptSaveEvent, preprocessEventData, calculateRecurringEventFrequency, deleteEventAndAllFollowing, deleteAllRecurringEvents, getBonnerEvents,addEventView, getEventRsvpCountsForTerm
from app.logic.participants import getEventParticipants, getParticipationStatusForTrainings, checkUserRsvp
from app.logic.fileHandler import FileHandler
from app.logic.bonner import getBonnerCohorts, makeBonnerXls, rsvpForBonnerCohort
from app.controllers.admin import admin_bp
from app.logic.manageSLFaculty import getInstructorCourses
from app.logic.courseManagement import unapprovedCourses, approvedCourses
from app.logic.serviceLearningCoursesData import parseUploadedFile, saveCourseParticipantsToDatabase



@admin_bp.route('/switch_user', methods=['POST'])
def switchUser():
    if app.env == "production":
        print(f"An attempt was made to switch to another user by {g.current_user.username}!")
        abort(403)

    print(f"Switching user from {g.current_user} to",request.form['newuser'])
    session['current_user'] = model_to_dict(User.get_by_id(request.form['newuser']))

    return redirect(request.referrer)


@admin_bp.route('/eventTemplates')
def templateSelect():
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff:
        allprograms = getAllowedPrograms(g.current_user)
        visibleTemplates = getAllowedTemplates(g.current_user)
        return render_template("/events/template_selector.html",
                                programs=allprograms,
                                celtsSponsoredProgram = Program.get(Program.isOtherCeltsSponsored),
                                templates=visibleTemplates)
    else:
        abort(403)


@admin_bp.route('/eventTemplates/<templateid>/<programid>/create', methods=['GET','POST'])
def createEvent(templateid, programid):
    if not (g.current_user.isAdmin or g.current_user.isProgramManagerFor(programid)):
        abort(403)

    # Validate given URL
    program = None
    try:
        template = EventTemplate.get_by_id(templateid)
        if programid:
            program = Program.get_by_id(programid)
    except DoesNotExist as e:
        print("Invalid template or program id:", e)
        flash("There was an error with your selection. Please try again or contact Systems Support.", "danger")
        return redirect(url_for("admin.program_picker"))

    # Get the data from the form or from the template
    eventData = template.templateData

    eventData['program'] = program

    if request.method == "GET":
        eventData['contactName'] = "CELTS Admin"
        eventData['contactEmail'] = app.config['celts_admin_contact']
        if program:
            eventData['location'] = program.defaultLocation
            if program.contactName:
                eventData['contactName'] = program.contactName
            if program.contactEmail:
                eventData['contactEmail'] = program.contactEmail

    # Try to save the form
    if request.method == "POST":
        eventData.update(request.form.copy())
        try:
            savedEvents, validationErrorMessage = attemptSaveEvent(eventData, getFilesFromRequest(request))

        except Exception as e:
            print("Error saving event:", e)
            savedEvents = False
            validationErrorMessage = "Unknown Error Saving Event. Please try again"

        if savedEvents:
            rsvpcohorts = request.form.getlist("cohorts[]")
            for year in rsvpcohorts:
                rsvpForBonnerCohort(int(year), savedEvents[0].id)

            noun = (eventData['isRecurring'] == 'on' and "Events" or "Event") # pluralize
            flash(f"{noun} successfully created!", 'success')

            if program:
                if len(savedEvents) > 1:
                    createAdminLog(f"Created a recurring event, <a href=\"{url_for('admin.eventDisplay', eventId = savedEvents[0].id)}\">{savedEvents[0].name}</a>, for {program.programName}, with a start date of {datetime.strftime(eventData['startDate'], '%m/%d/%Y')}. The last event in the series will be on {datetime.strftime(savedEvents[-1].startDate, '%m/%d/%Y')}.")
                else:
                    createAdminLog(f"Created <a href=\"{url_for('admin.eventDisplay', eventId = savedEvents[0].id)}\">{savedEvents[0].name}</a> for {program.programName}, with a start date of {datetime.strftime(eventData['startDate'], '%m/%d/%Y')}.")
            else:
                createAdminLog(f"Created a non-program event, <a href=\"{url_for('admin.eventDisplay', eventId = savedEvents[0].id)}\">{savedEvents[0].name}</a>, with a start date of {datetime.strftime(eventData['startDate'], '%m/%d/%Y')}.")

            return redirect(url_for("admin.eventDisplay", eventId = savedEvents[0].id))
        else:
            flash(validationErrorMessage, 'warning')

    # make sure our data is the same regardless of GET or POST
    preprocessEventData(eventData)
    isProgramManager = g.current_user.isProgramManagerFor(programid)

    futureTerms = selectSurroundingTerms(g.current_term, prevTerms=0)

    requirements, bonnerCohorts = [], []
    if eventData['program'] is not None and eventData['program'].isBonnerScholars:
        requirements = getCertRequirements(Certification.BONNER)
        bonnerCohorts = getBonnerCohorts(limit=5)
    return render_template(f"/admin/{template.templateFile}",
            template = template,
            eventData = eventData,
            futureTerms = futureTerms,
            requirements = requirements,
            bonnerCohorts = bonnerCohorts,
            isProgramManager = isProgramManager)


@admin_bp.route('/event/<eventId>/rsvp', methods=['GET'])
def rsvpLogDisplay(eventId):
    event = Event.get_by_id(eventId)
    eventData = model_to_dict(event, recurse=False)
    eventData['program'] = event.program
    isProgramManager = g.current_user.isProgramManagerFor(eventData['program'])
    if g.current_user.isCeltsAdmin or (g.current_user.isCeltsStudentStaff and isProgramManager):
        allLogs = EventRsvpLog.select(EventRsvpLog, User).join(User).where(EventRsvpLog.event_id == eventId).order_by(EventRsvpLog.createdOn.desc())
        return render_template("/events/rsvpLog.html",
                                event = event,
                                eventData = eventData,
                                allLogs = allLogs)
    else:
        abort(403)


@admin_bp.route('/event/<eventId>/view', methods=['GET'])
@admin_bp.route('/event/<eventId>/edit', methods=['GET','POST'])
def eventDisplay(eventId):
    pageViewsCount = EventView.select().where(EventView.event == eventId).count()
    if request.method == 'GET' and request.path == f'/event/{eventId}/view':
        viewer = g.current_user
        event = Event.get_by_id(eventId)
        addEventView(viewer,event) 
    # Validate given URL
    try:
        event = Event.get_by_id(eventId)
    except DoesNotExist as e:
        print(f"Unknown event: {eventId}")
        abort(404)

    notPermitted = not (g.current_user.isCeltsAdmin or g.current_user.isProgramManagerForEvent(event))
    if 'edit' in request.url_rule.rule and notPermitted:
        abort(403)

    eventData = model_to_dict(event, recurse=False)
    associatedAttachments = AttachmentUpload.select().where(AttachmentUpload.event == event)
    filepaths = FileHandler(eventId=event.id).retrievePath(associatedAttachments)

    image = None
    picurestype = [".jpeg", ".png", ".gif", ".jpg", ".svg", ".webp"]
    for attachment in associatedAttachments:
        for extension in picurestype:
            if (attachment.fileName.endswith(extension) and attachment.isDisplayed == True):
                image = filepaths[attachment.fileName][0]
        if image:
            break

                
    if request.method == "POST": # Attempt to save form
        eventData = request.form.copy()
        try:
            savedEvents, validationErrorMessage = attemptSaveEvent(eventData, getFilesFromRequest(request))

        except Exception as e:
            print("Error saving event:", e)
            savedEvents = False
            validationErrorMessage = "Unknown Error Saving Event. Please try again"


        if savedEvents:
            rsvpcohorts = request.form.getlist("cohorts[]")
            for year in rsvpcohorts:
                rsvpForBonnerCohort(int(year), event.id)

            flash("Event successfully updated!", "success")
            return redirect(url_for("admin.eventDisplay", eventId = event.id))
        else:
            flash(validationErrorMessage, 'warning')

    # make sure our data is the same regardless of GET and POST
    preprocessEventData(eventData)
    eventData['program'] = event.program
    futureTerms = selectSurroundingTerms(g.current_term)
    userHasRSVPed = checkUserRsvp(g.current_user, event) 
    filepaths = FileHandler(eventId=event.id).retrievePath(associatedAttachments)
    isProgramManager = g.current_user.isProgramManagerFor(eventData['program'])
    requirements, bonnerCohorts = [], []
    
    if eventData['program'] and eventData['program'].isBonnerScholars:
        requirements = getCertRequirements(Certification.BONNER)
        bonnerCohorts = getBonnerCohorts(limit=5)
    
    rule = request.url_rule

    # Event Edit
    if 'edit' in rule.rule:
        return render_template("admin/createEvent.html",
                                eventData = eventData,
                                futureTerms=futureTerms,
                                event = event,
                                requirements = requirements,
                                bonnerCohorts = bonnerCohorts,
                                userHasRSVPed = userHasRSVPed,
                                isProgramManager = isProgramManager,
                                filepaths = filepaths)
    # Event View
    else:
        # get text representations of dates
        eventData['timeStart'] = event.timeStart.strftime("%-I:%M %p")
        eventData['timeEnd'] = event.timeEnd.strftime("%-I:%M %p")
        eventData["startDate"] = event.startDate.strftime("%m/%d/%Y")

        # Identify the next event in a recurring series
        if event.recurringId:
            eventSeriesList = list(Event.select().where(Event.recurringId == event.recurringId)
                                        .where((Event.isCanceled == False) | (Event.id == event.id))
                                        .order_by(Event.startDate))
            eventIndex = eventSeriesList.index(event)
            if len(eventSeriesList) != (eventIndex + 1):
                eventData["nextRecurringEvent"] = eventSeriesList[eventIndex + 1]

        currentEventRsvpAmount = getEventRsvpCountsForTerm(g.current_term)

        userParticipatedTrainingEvents = getParticipationStatusForTrainings(eventData['program'], [g.current_user], g.current_term)

        return render_template("eventView.html",
                                eventData = eventData,
                                event = event,
                                userHasRSVPed = userHasRSVPed,
                                programTrainings = userParticipatedTrainingEvents,
                                currentEventRsvpAmount = currentEventRsvpAmount,
                                isProgramManager = isProgramManager,
                                filepaths = filepaths,
                                image = image,
                                pageViewsCount= pageViewsCount)


@admin_bp.route('/event/<eventId>/cancel', methods=['POST'])
def cancelRoute(eventId):
    if g.current_user.isAdmin:
        try:
            cancelEvent(eventId)
            return redirect(request.referrer)

        except Exception as e:
            print('Error while canceling event:', e)
            return "", 500
        
    else:
        abort(403)
    
@admin_bp.route('/event/<eventId>/delete', methods=['POST'])
def deleteRoute(eventId):
    try:
        deleteEvent(eventId)
        flash("Event successfully deleted.", "success")
        return redirect(url_for("main.events", selectedTerm=g.current_term))

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500
@admin_bp.route('/event/<eventId>/deleteEventAndAllFollowing', methods=['POST'])
def deleteEventAndAllFollowingRoute(eventId):
    try:
        deleteEventAndAllFollowing(eventId)
        flash("Events successfully deleted.", "success")
        return redirect(url_for("main.events", selectedTerm=g.current_term))

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500
@admin_bp.route('/event/<eventId>/deleteAllRecurring', methods=['POST'])
def deleteAllRecurringEventsRoute(eventId):
    try:
        deleteAllRecurringEvents(eventId)
        flash("Events successfully deleted.", "success")
        return redirect(url_for("main.events", selectedTerm=g.current_term))

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500

@admin_bp.route('/makeRecurringEvents', methods=['POST'])
def addRecurringEvents():
    recurringEvents = calculateRecurringEventFrequency(preprocessEventData(request.form.copy()))
    return json.dumps(recurringEvents, default=str)


@admin_bp.route('/userProfile', methods=['POST'])
def userProfile():
    volunteerName= request.form.copy()
    if volunteerName['searchStudentsInput']:
        username = volunteerName['searchStudentsInput'].strip("()")
        user=username.split('(')[-1]
        return redirect(url_for('main.viewUsersProfile', username=user))
    else:
        flash(f"Please enter the first name or the username of the student you would like to search for.", category='danger')
        return redirect(url_for('admin.studentSearchPage'))

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    if g.current_user.isAdmin:
        return render_template("/admin/searchStudentPage.html")
    abort(403)

@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():
    '''Renders the page, will be removed once merged with full page'''

    return render_template('addParticipants.html',
                            title="Add Participants")

@admin_bp.route('/adminLogs', methods = ['GET', 'POST'])
def adminLogs():
    if g.current_user.isCeltsAdmin:
        allLogs = AdminLog.select(AdminLog, User).join(User).order_by(AdminLog.createdOn.desc())
        return render_template("/admin/adminLogs.html",
                                allLogs = allLogs)
    else:
        abort(403)

@admin_bp.route("/deleteEventFile", methods=["POST"])
def deleteEventFile():
    fileData= request.form
    eventfile=FileHandler(eventId=fileData["databaseId"])
    eventfile.deleteFile(fileData["fileId"])
    return ""

@admin_bp.route("/uploadCourseParticipant", methods= ["POST"])
def addCourseFile():
    fileData = request.files['addCourseParticipants']
    filePath = os.path.join(app.config["files"]["base_path"], fileData.filename)
    fileData.save(filePath)
    (session['cpPreview'], session['cpErrors']) = parseUploadedFile(filePath)
    os.remove(filePath)
    return redirect(url_for("admin.manageServiceLearningCourses"))

@admin_bp.route('/manageServiceLearning', methods = ['GET', 'POST'])
@admin_bp.route('/manageServiceLearning/<term>', methods = ['GET', 'POST'])
def manageServiceLearningCourses(term=None):
    """
    The SLC management page for admins
    """
    if not g.current_user.isCeltsAdmin:
        abort(403) 

    if request.method =='POST' and "submitParticipant" in request.form:
        saveCourseParticipantsToDatabase(session.pop('cpPreview', {}))
        flash('Courses and participants saved successfully!', 'success')
        return redirect(url_for('admin.manageServiceLearningCourses'))

    manageTerm = Term.get_or_none(Term.id == term) or g.current_term

    setRedirectTarget(request.full_path)

    return render_template('/admin/manageServiceLearningFaculty.html',
                            courseInstructors = getInstructorCourses(),
                            unapprovedCourses = unapprovedCourses(term),
                            approvedCourses = approvedCourses(term),
                            terms = selectSurroundingTerms(g.current_term),
                            term = manageTerm,
                            cpPreview= session.get('cpPreview',{}),
                            cpPreviewErrors = session.get('cpErrors',[])
                           )

@admin_bp.route("/deleteUploadedFile", methods= ["POST"])
def removeFromSession():
    try:
        session.pop('cpPreview')
    except KeyError:
        pass

    return ""

@admin_bp.route("/manageBonner")
def manageBonner():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    return render_template("/admin/bonnerManagement.html",
                           cohorts=getBonnerCohorts(),
                           events=getBonnerEvents(g.current_term),
                           requirements = getCertRequirements(certification=Certification.BONNER))

@admin_bp.route("/bonner/<year>/<method>/<username>", methods=["POST"])
def updatecohort(year, method, username):
    if not g.current_user.isCeltsAdmin:
        abort(403)

    try:
        user = User.get_by_id(username)
    except:
        abort(500)

    if method == "add":
        try:
            BonnerCohort.create(year=year, user=user)
            flash(f"Successfully added {user.fullName} to {year} Bonner Cohort.", "success")
        except IntegrityError as e:
            # if they already exist, ignore the error
            flash(f'Error: {user.fullName} already added.', "danger")
            pass
        
    elif method == "remove":
        BonnerCohort.delete().where(BonnerCohort.user == user, BonnerCohort.year == year).execute()
        flash(f"Successfully removed {user.fullName} from {year} Bonner Cohort.", "success")
    else:
        flash(f"Error: {user.fullName} can't be added.", "danger")
        abort(500)

    return ""

@admin_bp.route("/bonnerxls")
def bonnerxls():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newfile = makeBonnerXls()
    return send_file(open(newfile, 'rb'), download_name='BonnerStudents.xlsx', as_attachment=True)

@admin_bp.route("/saveRequirements/<certid>", methods=["POST"])
def saveRequirements(certid):
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newRequirements = updateCertRequirements(certid, request.get_json())

    return jsonify([requirement.id for requirement in newRequirements])


@admin_bp.route("/displayEventFile", methods=["POST"])
def displayEventFile():
    fileData= request.form
    eventfile=FileHandler(eventId=fileData["id"])
    eventfile.changeDisplay(fileData['id'])
    return ""
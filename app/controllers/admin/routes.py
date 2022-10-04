from flask import request, render_template, url_for, g, Flask, redirect
from flask import flash, abort, jsonify, session, send_file
from peewee import DoesNotExist, fn, IntegrityError
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
from datetime import datetime, date
from dateutil import parser

from app import app
from app.models.program import Program
from app.models.programManager import ProgramManager
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models.term import Term
from app.models.eventTemplate import EventTemplate
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.models.adminLogs import AdminLogs
from app.models.eventFile import EventFile
from app.models.bonnerCohort import BonnerCohort
from app.models.certification import Certification

from app.logic.userManagement import getAllowedPrograms, getAllowedTemplates
from app.logic.adminLogs import createLog
from app.logic.certification import getCertRequirements, updateCertRequirements
from app.logic.volunteers import getEventLengthInHours
from app.logic.utils import selectSurroundingTerms
from app.logic.events import deleteEvent, attemptSaveEvent, preprocessEventData, calculateRecurringEventFrequency, getBonnerEvents
from app.logic.participants import getEventParticipants, getUserParticipatedEvents, checkUserRsvp, checkUserVolunteer
from app.logic.fileHandler import FileHandler
from app.logic.bonner import getBonnerCohorts, makeBonnerXls
from app.controllers.admin import admin_bp
from app.controllers.admin.volunteers import getVolunteers
from app.controllers.admin.userManagement import manageUsers


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
                                templates=visibleTemplates)
    else:
        abort(403)


@admin_bp.route('/eventTemplates/<templateid>/create', methods=['GET','POST'])
@admin_bp.route('/eventTemplates/<templateid>/<programid>/create', methods=['GET','POST'])
def createEvent(templateid, programid=None):
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
    if request.method == "POST":
        attachmentFiles = request.files.getlist("attachmentObject")
        fileDoesNotExist = attachmentFiles[0].content_type == "application/octet-stream"
        if fileDoesNotExist:
            attachmentFiles = None
        eventData.update(request.form.copy())

    if program:
        eventData["program"] = program

    if request.method == "GET":
        eventData['contactName'] = "CELTS Admin"
        eventData['contactEmail'] = app.config['celts_admin_contact']
        if program:
            if program.contactName and program.contactEmail:
                eventData['contactName'] = program.contactName
                eventData['contactEmail'] = program.contactEmail

    # Try to save the form
    if request.method == "POST":
        try:
            savedEvents, validationErrorMessage = attemptSaveEvent(eventData, attachmentFiles)

        except Exception as e:
            print("Error saving event:", e)
            savedEvents = False
            validationErrorMessage = "Unknown Error Saving Event. Please try again"

        if savedEvents:

            noun = (eventData['isRecurring'] == 'on' and "Events" or "Event") # pluralize
            flash(f"{noun} successfully created!", 'success')

            if program:
                if len(savedEvents) > 1:
                    createLog(f"Created a recurring event, <a href=\"{url_for('admin.eventDisplay', eventId = savedEvents[0].id)}\">{savedEvents[0].name}</a>, for {program.programName}, with a start date of {datetime.strftime(eventData['startDate'], '%m/%d/%Y')}. The last event in the series will be on {datetime.strftime(savedEvents[-1].startDate, '%m/%d/%Y')}.")
                else:
                    createLog(f"Created <a href=\"{url_for('admin.eventDisplay', eventId = savedEvents[0].id)}\">{savedEvents[0].name}</a> for {program.programName}, with a start date of {datetime.strftime(eventData['startDate'], '%m/%d/%Y')}.")
            else:
                createLog(f"Created a non-program event, <a href=\"{url_for('admin.eventDisplay', eventId = savedEvents[0].id)}\">{savedEvents[0].name}</a>, with a start date of {datetime.strftime(eventData['startDate'], '%m/%d/%Y')}.")

            return redirect(url_for("admin.eventDisplay", eventId = savedEvents[0].id))
        else:
            flash(validationErrorMessage, 'warning')

    # make sure our data is the same regardless of GET or POST
    preprocessEventData(eventData)
    isProgramManager = g.current_user.isProgramManagerFor(programid)

    futureTerms = selectSurroundingTerms(g.current_term, prevTerms=0)

    requirements = bonnerCohorts = []
    if 'program' in eventData and eventData['program'].isBonnerScholars:
        requirements = getCertRequirements(Certification.BONNER)
        bonnerCohorts = getBonnerCohorts(limit=5)

    return render_template(f"/admin/{template.templateFile}",
            template = template,
            eventData = eventData,
            futureTerms = futureTerms,
            requirements = requirements,
            bonnerCohorts = bonnerCohorts,
            isProgramManager = isProgramManager)

@admin_bp.route('/eventsList/<eventId>/view', methods=['GET'])
@admin_bp.route('/eventsList/<eventId>/edit', methods=['GET','POST'])
def eventDisplay(eventId):
    if 'edit' in request.url_rule.rule and not (g.current_user.isCeltsAdmin or g.current_user.isProgramManagerForEvent(eventId)):
        abort(403)

    # Validate given URL
    try:
        event = Event.get_by_id(eventId)
    except DoesNotExist as e:
        print(f"Unknown event: {eventId}")
        abort(404)
    eventData = model_to_dict(event, recurse=False)
    associatedAttachments = EventFile.select().where(EventFile.event == event)

    if request.method == "POST": # Attempt to save form
        eventData = request.form.copy()
        attachmentFiles = request.files.getlist("attachmentObject")
        savedEvents, validationErrorMessage = attemptSaveEvent(eventData, attachmentFiles)
        if savedEvents:
            flash("Event successfully updated!", "success")
            return redirect(url_for("admin.eventDisplay", eventId = event.id))
        else:
            flash(validationErrorMessage, 'warning')

    # make sure our data is the same regardless of GET and POST
    preprocessEventData(eventData)
    eventData['program'] = event.singleProgram
    futureTerms = selectSurroundingTerms(g.current_term)
    userHasRSVPed = checkUserRsvp(g.current_user, event)
    isPastEvent = event.isPast
    filepaths =FileHandler().retrievePath(associatedAttachments, event.id)
    isProgramManager = g.current_user.isProgramManagerFor(eventData['program'])

    requirements = []
    if eventData['program'] and eventData['program'].isBonnerScholars:
        requirements = getCertRequirements(Certification.BONNER)
        bonnerCohorts = getBonnerCohorts(limit=5)

    rule = request.url_rule
    # Event Edit
    if 'edit' in rule.rule:
        return render_template("admin/createEvent.html",
                                eventData = eventData,
                                futureTerms=futureTerms,
                                isPastEvent = isPastEvent,
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
            eventSeriesList = list(Event.select().where(Event.recurringId == event.recurringId).order_by(Event.startDate))
            eventIndex = eventSeriesList.index(event)
            if len(eventSeriesList) != (eventIndex + 1):
                eventData["nextRecurringEvent"] = eventSeriesList[eventIndex + 1]

        userParticipatedEvents = getUserParticipatedEvents(eventData['program'], g.current_user, g.current_term)
        return render_template("eventView.html",
                                eventData = eventData,
                                isPastEvent = isPastEvent,
                                userHasRSVPed = userHasRSVPed,
                                programTrainings = userParticipatedEvents,
                                isProgramManager = isProgramManager,
                                filepaths = filepaths)

@admin_bp.route('/event/<eventId>/delete', methods=['POST'])
def deleteRoute(eventId):
    try:
        deleteEvent(eventId)
        flash("Event successfully deleted.", "success")
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
    username = volunteerName['searchStudentsInput'].strip("()")
    user=username.split('(')[-1]
    return redirect(url_for('main.viewUsersProfile', username=user))

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
        allLogs = AdminLogs.select(AdminLogs, User).join(User).order_by(AdminLogs.createdOn.desc())
        return render_template("/admin/adminLogs.html",
                                allLogs = allLogs)
    else:
        abort(403)

@admin_bp.route("/deleteFile", methods=["POST"])
def deleteFile():
    fileData= request.form
    eventfile=FileHandler()
    eventfile.deleteEventFile(fileData["fileId"],fileData["eventId"])
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
        except IntegrityError as e:
            # if they already exist, ignore the error
            pass
    elif method == "remove":
        BonnerCohort.delete().where(BonnerCohort.user == user, BonnerCohort.year == year).execute()
    else:
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

    return jsonify([req.id for req in newRequirements])

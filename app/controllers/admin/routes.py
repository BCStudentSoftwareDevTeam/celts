from flask import request, render_template, url_for, g, Flask, redirect, flash, abort, json, jsonify, session
from peewee import DoesNotExist, fn
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
from datetime import datetime, date
from dateutil import parser
from app import app
from app.models.program import Program
from app.models.event import Event
from app.models.facilitator import EventFacilitator
from app.models.eventParticipant import EventParticipant
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.eventTemplate import EventTemplate
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.models.adminLogs import AdminLogs
from app.logic.volunteers import getEventLengthInHours, isProgramManagerForEvent
from app.logic.utils import selectSurroundingTerms
from app.logic.events import deleteEvent, getAllFacilitators, attemptSaveEvent, preprocessEventData, calculateRecurringEventFrequency
from app.logic.courseManagement import pendingCourses, approvedCourses
from app.logic.participants import getEventParticipants, getUserParticipatedEvents
from app.controllers.admin import admin_bp
from app.controllers.admin.volunteers import getVolunteers
from app.controllers.admin.userManagement import manageUsers
from app.logic.userManagement import getAllowedPrograms, getAllowedTemplates


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

    # Get the data for the form, from the template or the form submission
    eventData = template.templateData
    if request.method == "POST":
        print("++++++++++++++++++++++++++++++++++")
        attachmentFiles = request.files.getlist("attachmentObject")
        eventData = request.form.copy()
        print(eventData)
        print(attachmentFiles)
    if program:
        # TODO need to handle the multiple programs case
        eventData["program"] = program

    # Try to save the form
    if request.method == "POST":
        try:
            saveSuccess, validationErrorMessage = attemptSaveEvent(eventData, attachmentFiles)
        except Exception as e:
            print("Error saving event:", e)
            saveSuccess = False
            validationErrorMessage = "Unknown Error Saving Event. Please try again"

        if saveSuccess:
            noun = (eventData['isRecurring'] == 'on' and "Events" or "Event") # pluralize
            flash(f"{noun} successfully created!", 'success')
            eventId = Event.select(fn.MAX(Event.id)).scalar()
            return redirect(url_for("admin.eventDisplay", eventId = eventId))
        else:
            flash(validationErrorMessage, 'warning')

    # make sure our data is the same regardless of GET or POST
    preprocessEventData(eventData)
    isProgramManager = g.current_user.isProgramManagerFor(programid)

    futureTerms = selectSurroundingTerms(g.current_term, prevTerms=0)

    return render_template(f"/admin/{template.templateFile}",
            template = template,
            eventData = eventData,
            futureTerms = futureTerms,
            allFacilitators = getAllFacilitators(),
            isProgramManager = isProgramManager)

@admin_bp.route('/eventsList/<eventId>/view', methods=['GET'])
@admin_bp.route('/eventsList/<eventId>/edit', methods=['GET','POST'])
def eventDisplay(eventId):
    if request.method == "POST" and not (g.current_user.isCeltsAdmin or isProgramManagerForEvent(g.current_user, eventId)):
        abort(403)

    # Validate given URL
    try:
        event = Event.get_by_id(eventId)
    except DoesNotExist as e:
        print(f"Unknown event: {eventId}")
        abort(404)

    eventData = model_to_dict(event, recurse=False)
    if request.method == "POST": # Attempt to save form
        eventData = request.form.copy()
        saveSuccess, validationErrorMessage = attemptSaveEvent(eventData, attemptSaveEvent)
        if saveSuccess:
            flash("Event successfully updated!", "success")
            return redirect(url_for("admin.eventDisplay", eventId = eventId))
        else:
            flash(validationErrorMessage, 'warning')

    preprocessEventData(eventData)
    futureTerms = selectSurroundingTerms(g.current_term)
    userHasRSVPed = EventRsvp.get_or_none(EventRsvp.user == g.current_user, EventRsvp.event == event)
    isPastEvent = (datetime.now() >= datetime.combine(event.startDate, event.timeStart))
    program = event.singleProgram
    isProgramManager = g.current_user.isProgramManagerFor(program)
    rule = request.url_rule
    if 'edit' in rule.rule:
        if not (g.current_user.isCeltsAdmin or isProgramManager):
            abort(403)
        return render_template("admin/createEvent.html",
                                eventData = eventData,
                                allFacilitators = getAllFacilitators(),
                                futureTerms=futureTerms,
                                isPastEvent = isPastEvent,
                                userHasRSVPed = userHasRSVPed,
                                isProgramManager = isProgramManager)
    else:
        eventFacilitators = EventFacilitator.select().where(EventFacilitator.event == event)
        eventFacilitatorNames = [eventFacilitator.user for eventFacilitator in eventFacilitators]
        eventData['timeStart'] = event.timeStart.strftime("%-I:%M %p")
        eventData['timeEnd'] = event.timeEnd.strftime("%-I:%M %p")
        eventData["startDate"] = event.startDate.strftime("%m/%d/%Y")
        programManager = ProgramManager.get_or_none(program=program)
        userParticipatedEvents = getUserParticipatedEvents(program, g.current_user)
        return render_template("eventView.html",
                                eventData = eventData,
                                eventFacilitatorNames = eventFacilitatorNames,
                                isPastEvent = isPastEvent,
                                userHasRSVPed = userHasRSVPed,
                                programTrainings = userParticipatedEvents,
                                programManager = programManager,
                                isProgramManager = isProgramManager)

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


@admin_bp.route('/volunteerProfile', methods=['POST'])
def volunteerProfile():
    volunteerName= request.form.copy()
    username = volunteerName['searchStudentsInput'].strip("()")
    user=username.split('(')[-1]
    return redirect(url_for('main.viewVolunteersProfile', username=user))

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    if g.current_user.isAdmin:
        return render_template("/searchStudentPage.html")
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

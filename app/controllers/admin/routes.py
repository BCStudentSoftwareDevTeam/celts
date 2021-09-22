from flask import request, render_template, url_for, g, Flask, redirect, flash, abort, json, jsonify
from playhouse.shortcuts import model_to_dict
import json

from datetime import datetime
from dateutil import parser

from app.models.program import Program
from app.models.event import Event
from app.models.facilitator import Facilitator
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.term import Term
from app.models.eventTemplate import EventTemplate
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent

from app.logic.participants import trainedParticipants
from app.logic.volunteers import getEventLengthInHours
from app.logic.utils import selectFutureTerms
from app.logic.searchUsers import searchUsers
from app.logic.events import deleteEvent, getAllFacilitators, eventEdit
from app.logic.eventCreation import createNewEvent, setValueForUncheckedBox, calculateRecurringEventFrequency
from app.logic.eventCreation import validateNewEventData
from app.controllers.admin import admin_bp
from app.controllers.admin.volunteers import getVolunteers

@admin_bp.route('/template_select')
def program_picker():
    allprograms = Program.select().order_by(Program.programName)
    visibleTemplates = EventTemplate.select().where(EventTemplate.isVisible==True).order_by(EventTemplate.name)

    return render_template("/events/template_selector.html",
                programs=allprograms,
                templates=visibleTemplates
            )

@admin_bp.route('/event/<templateid>/create')
@admin_bp.route('/event/<templateid>/<programid>/create')
def template_select(templateid, programid=None):
    if not (g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff):
        abort(403)

    program = None
    try:
        template = EventTemplate.get_by_id(templateid)
        if programid:
            program = Program.get_by_id(programid)

    except DoesNotExist as e:
        print("Invalid template or program id:", e)
        flash("There was an error with your selection. Please try again or contact Systems Support.", "danger")
        return redirect(url_for("admin.program_picker"))

    futureTerms = selectFutureTerms(g.current_term)

    eventData = template.templateData
    if program:
        eventData["program"] = program

    return render_template(f"/admin/{template.templateFile}", 
            template = template,
            eventData = eventData,
            futureTerms = futureTerms,
            facilitators = getAllFacilitators(),
            eventFacilitators = [])


@admin_bp.route('/event/<eventId>/edit', methods=['GET'])
def editEvent(eventId):
    try:
        event = Event.get_by_id(eventId)
    except DoesNotExist as e:
        print(f"Unknown event: {eventId}")
        abort(404)

    facilitators = getAllFacilitators()
    eventFacilitators = Facilitator.select().where(Facilitator.event == event)
    futureTerms = selectFutureTerms(g.current_term)
    userHasRSVPed = EventParticipant.get_or_none(EventParticipant.user == g.current_user, EventParticipant.event == event)
    isPastEvent = (datetime.now() >= datetime.combine(event.startDate, event.timeStart))

    return render_template("admin/createSingleEvent.html",
                            eventData = model_to_dict(event),
                            facilitators = facilitators,
                            eventFacilitators = eventFacilitators,
                            futureTerms = futureTerms,
                            isPastEvent = isPastEvent,
                            userHasRSVPed = userHasRSVPed)

@admin_bp.route('/event/<eventId>/delete', methods=['POST'])
def deleteRoute(eventId):

    try:
        eventTerm = Event.get(Event.id == eventId).term
        deleteEvent(eventId)
        flash("Event removed", "success")
        return redirect(url_for("events.events", term=eventTerm))

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500

@admin_bp.route('/makeRecurringEvents', methods=['POST'])
def addRecurringEvents():
    recurringEventInfo = request.form.copy()
    recurringEvents = calculateRecurringEventFrequency(recurringEventInfo)
    return json.dumps(recurringEvents)

@admin_bp.route('/createEvent', methods=['POST'])
def createEvent():

    if not (g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff):
        flash("Only celts admins can create an event!", 'warning')
        return redirect(url_for("main.profilePage", username = g.current_user.username))

    else:
        eventData = request.form.copy() # request.form returns a immutable dict so we need to copy to make changes
        newEventData= setValueForUncheckedBox(eventData)
        eventId = newEventData['eventId']

        #if an event is not recurring then it will have same end and start date
        if newEventData['eventEndDate'] == '':
            newEventData['eventEndDate'] = newEventData['eventStartDate']

        # function to validate data
        if eventId:
            dataIsValid, validationErrorMessage, newEventData = validateNewEventData(newEventData, checkExists=False)
        else:
            dataIsValid, validationErrorMessage, newEventData = validateNewEventData(newEventData)

        if dataIsValid:
            if not eventId:
                createNewEvent(newEventData)
                flash("Event successfully created!", 'success')
                return redirect(url_for("events.events", term = newEventData['eventTerm']))
            else:
                eventEdit(newEventData)
                flash("Event successfully updated!", "success")
                return redirect(url_for("events.events", term = newEventData['eventTerm']))
        else:
            flash(validationErrorMessage, 'warning')
            return redirect(url_for("admin.createEventPage", program = newEventData['programId']))

@admin_bp.route('/volunteerProfile', methods=['POST'])
def volunteerProfile():
    volunteerName= request.form.copy()
    username = volunteerName['searchStudentsInput'].strip("()")
    user=username.split('(')[-1]
    return redirect(url_for('main.profilePage', username=user))

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff:
        return render_template("/searchStudentPage.html")
    abort(403)

@admin_bp.route('/searchStudents/<query>', methods = ['GET'])
def searchStudents(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    try:
        query = query.strip()
        search = query.upper()
        splitSearch = search.split()
        searchResults = searchUsers(query)
        return searchResults
    except Exception as e:
        print(e)
        return "Error Searching Volunteers query", 500

@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():
    '''Renders the page, will be removed once merged with full page'''

    return render_template('addParticipants.html',
                            title="Add Participants")

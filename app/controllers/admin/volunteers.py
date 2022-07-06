import re
from flask import request, render_template, redirect, url_for, request, flash, abort, g, json, jsonify
from datetime import datetime
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateEventParticipants, addVolunteerToEventRsvp, getEventLengthInHours,setUserBackgroundCheck, setProgramManager, isProgramManagerForEvent
from app.logic.participants import trainedParticipants, getEventParticipants
from app.logic.events import getPreviousRecurringEventData
from app.models.user import User
from app.models.eventRsvp import EventRsvp
from app.models.backgroundCheck import BackgroundCheck
from app.models.programManager import ProgramManager
from app.logic.adminLogs import createLog



@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def getVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    return json.dumps(searchUsers(query))

@admin_bp.route('/eventsList/<eventID>/track_volunteers', methods=['GET'])
def trackVolunteersPage(eventID):
    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}")
        abort(404)

    program = event.singleProgram

    # TODO: What do we do for no programs or multiple programs?
    if not program:
        return "TODO: What do we do for no programs or multiple programs?"

    trainedParticipantsList = trainedParticipants(program, g.current_term)
    eventParticipants = getEventParticipants(event)
    isProgramManager = isProgramManagerForEvent(g.current_user, event)

    if not (g.current_user.isCeltsAdmin or (g.current_user.isCeltsStudentStaff and isProgramManager)):
        abort(403)

    eventRsvpData = (EventRsvp
        .select()
        .where(EventRsvp.event==event))

    eventLengthInHours = getEventLengthInHours(
        event.timeStart,
        event.timeEnd,
        event.startDate)

    recurringEventID = event.recurringId # query Event Table to get recurringId using Event ID.
    recurringEventStartDate = event.startDate
    recurringVolunteers = getPreviousRecurringEventData(recurringEventID)
    return render_template("/events/trackVolunteers.html",
        eventRsvpData=list(eventRsvpData),
        eventParticipants=eventParticipants,
        eventLength=eventLengthInHours,
        program=program,
        event=event,
        recurringEventID = recurringEventID,
        recurringEventStartDate = recurringEventStartDate,
        recurringVolunteers = recurringVolunteers,
        trainedParticipantsList=trainedParticipantsList)

@admin_bp.route('/eventsList/<eventID>/track_volunteers', methods=['POST'])
def updateVolunteerTable(eventID):
    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}")
        abort(404)

    program = event.singleProgram
    # TODO: What do we do for no programs or multiple programs?
    if not program:
        return "TODO: What do we do for no programs or multiple programs?"

    volunteerUpdated = updateEventParticipants(request.form)
    if volunteerUpdated:
        flash("Volunteer table succesfully updated", "success")
    else:
        flash("Error adding volunteer", "danger")
    return redirect(url_for("admin.trackVolunteersPage", eventID=eventID))

@admin_bp.route('/addVolunteersToEvent/<eventId>', methods = ['POST'])
@admin_bp.route('/addVolunteerToEvent/<eventId>/<volunteer>', methods = ['POST'])
def addVolunteer(eventId, volunteer = None):
    data = request.form
    getRecurringId  = Event.select(Event.recurringId).where(Event.id == eventId).distinct()
    eventParticipants = getEventParticipants(eventId)
    if volunteer == None:
        successfullyAddedRecurringVolunteer = None
        if data["action"] == "add":
            if len(eventParticipants) == 0:
                successfullyAddedRecurringVolunteer = addVolunteerToEventRsvp(data["user"].username, eventId)
                EventParticipant.create(user = username, event = eventId)
            else:
                if EventRsvp.select(EventRsvp.user==data["user"].username, EventRsvp.event_id == eventId).exists():
                    print("This user has already been added to this event")
                else:
                    successfullyAddedRecurringVolunteer = addVolunteerToEventRsvp(data["user"].username, eventId)
                    EventParticipant.create(user = data["user"].username, event = eventId)
        else:
            return "Nothing yet!"

        if successfullyAddedRecurringVolunteer:
            flash("Volunteer successfully added!", "success")
        else:
            flash("Error when adding volunteer", "danger")
    else:
        username = volunteer.strip("()").split('(')[-1]
        user = User.get(User.username==username)
        successfullyAddedVolunteer = addVolunteerToEventRsvp(user, eventId)
        EventParticipant.create(user=user, event=eventId) # user is present
        if successfullyAddedVolunteer:
            flash("Volunteer successfully added!", "success")
        else:
            flash("Error when adding volunteer", "danger")
    return "recurring people have been added!"

@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user==user, EventParticipant.event==eventID)).execute()
    (EventRsvp.delete().where(EventRsvp.user==user)).execute()
    flash("Volunteer successfully removed", "success")
    return ""

@admin_bp.route('/updateBackgroundCheck', methods = ['POST'])
def updateBackgroundCheck():
    if g.current_user.isCeltsAdmin:
        eventData = request.form
        user = eventData['user']
        checkPassed = int(eventData['checkPassed'])
        type = eventData['bgType']
        dateCompleted = eventData['bgDate']
        setUserBackgroundCheck(user,type, checkPassed, dateCompleted)
        return " "

@admin_bp.route('/updateProgramManager', methods=["POST"])
def updateProgramManager():
    if g.current_user.isCeltsAdmin:
        data =request.form
        username = User.get(User.username == data["user_name"])
        event =Event.get_by_id(data['program_id'])
        setProgramManager(data["user_name"], data["program_id"], data["action"])
        createLog(f'{username.firstName} has been {data["action"]}ed as a Program Manager for {event.name}')
        return ""
    else:
        abort(403)

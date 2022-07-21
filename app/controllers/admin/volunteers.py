from flask import request, render_template, redirect, url_for, request, flash, abort, g, json, jsonify
from datetime import datetime
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateEventParticipants, addVolunteerToEventRsvp, getEventLengthInHours,setUserBackgroundCheck, setProgramManager
from app.logic.participants import trainedParticipants, getEventParticipants
from app.logic.events import getPreviousRecurringEventData
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
    trainedParticipantsList = trainedParticipants(program, g.current_term)
    eventParticipants = getEventParticipants(event)
    isProgramManager = g.current_user.isProgramManagerForEvent(event)

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

    volunteerUpdated = updateEventParticipants(request.form)
    if volunteerUpdated:
        flash("Volunteer table succesfully updated", "success")
    else:
        flash("Error adding volunteer", "danger")
    return redirect(url_for("admin.trackVolunteersPage", eventID=eventID))


@admin_bp.route('/addVolunteersToEvent/<eventId>', methods = ['POST'])
def addVolunteer(eventId):
    event = Event.get_by_id(eventId)
    successfullyAddedVolunteer = False
    usernameList = []
    eventParticipants = getEventParticipants(eventId)
    usernameList = request.form.getlist("volunteer[]")

    for user in usernameList:
        user = User.get(User.username==user)
        isVolunteerInEvent =  (EventRsvp.select().where(EventRsvp.user==user, EventRsvp.event_id == eventId).exists() and
              EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event_id == eventId).exists())

        if len(eventParticipants) == 0 or isVolunteerInEvent == False:
            addVolunteerToEventRsvp(user, eventId)
            EventParticipant.create(user = user, event = eventId)
            successfullyAddedVolunteer = True
        if isVolunteerInEvent:
            successfullyAddedVolunteer = True

    if len(usernameList) == 0:
        successfullyAddedVolunteer = False

    if (successfullyAddedVolunteer):
        flash("Volunteer added successfully.", "success")
    else:
        flash("Error when adding volunteer to event." ,"danger")

    if 'ajax' in request.form and request.form['ajax']:
        return ''

    return redirect(url_for('admin.trackVolunteersPage', eventID = eventId))


@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user==user, EventParticipant.event==eventID)).execute()
    (EventRsvp.delete().where(EventRsvp.user==user, EventRsvp.event==eventID)).execute()
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
@admin_bp.route("/updatePhone", methods=["POST"])
def updatePhone():
    newinfo=request.form
    User.update(phoneNumber=newinfo["phoneNumber"]).where(User.username==newinfo["username"]).execute()
    return ""
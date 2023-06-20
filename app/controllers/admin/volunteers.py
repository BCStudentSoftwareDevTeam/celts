from flask import request, render_template, redirect, url_for, request, flash, abort, g, json, jsonify
from datetime import datetime
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.program import Program
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateEventParticipants, addVolunteerToEventRsvp, getEventLengthInHours, addUserBackgroundCheck, setProgramManager
from app.logic.participants import trainedParticipants, getEventParticipants, addPersonToEvent
from app.logic.events import getPreviousRecurringEventData, getEventRsvpCountsForTerm
from app.models.eventRsvp import EventRsvp
from app.models.backgroundCheck import BackgroundCheck
from app.models.programManager import ProgramManager
from app.logic.adminLogs import createLog
from app.logic.users import getBannedUsers, isBannedFromEvent


@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def getVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    return json.dumps(searchUsers(query))

@admin_bp.route('/event/<eventID>/track_volunteers', methods=['POST'])
def updateVolunteerTable(eventID):
    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}")
        abort(404)

    volunteerUpdated = updateEventParticipants(request.form)
    if volunteerUpdated:
        flash("Volunteer table succesfully updated", "success")
    else:
        flash("Error adding volunteer", "danger")
    return redirect(url_for("admin.trackVolunteersPage", eventID=eventID))

@admin_bp.route('/event/<eventID>/track_volunteers', methods=['GET'])
def trackVolunteersPage(eventID):
    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}", e)
        abort(404)
    eventData = model_to_dict(event, recurse=False)
    eventData["program"] = event.singleProgram
    trainedParticipantsList = trainedParticipants(event.singleProgram, g.current_term)
    eventParticipants = getEventParticipants(event)
    isProgramManager = g.current_user.isProgramManagerForEvent(event)
    bannedUsers = [row.user for row in getBannedUsers(event.singleProgram)]
    if not (g.current_user.isCeltsAdmin or (g.current_user.isCeltsStudentStaff and isProgramManager)):
        abort(403)

    eventRsvpData = list(EventRsvp.select().where(EventRsvp.event==event).order_by(EventRsvp.rsvpTime))
    eventParticipantData = list(EventParticipant.select().where(EventParticipant.event==event))
    participantsAndRsvp = (eventParticipantData + eventRsvpData)
    eventVolunteerData = []
    volunteerUser = []
    for volunteer in participantsAndRsvp:
        if volunteer.user not in volunteerUser:
            eventVolunteerData.append(volunteer)
            volunteerUser.append(volunteer.user)
    eventWaitlistData = [volunteer for volunteer in eventVolunteerData if volunteer.rsvpWaitlist]
    eventLengthInHours = getEventLengthInHours(event.timeStart, event.timeEnd, event.startDate)

    recurringEventID = event.recurringId # query Event Table to get recurringId using Event ID.
    recurringEventStartDate = event.startDate
    recurringVolunteers = getPreviousRecurringEventData(recurringEventID)

    currentRsvpAmount = getEventRsvpCountsForTerm(g.current_term)

    return render_template("/events/trackVolunteers.html",
                            eventData = eventData,
                            eventVolunteerData = eventVolunteerData,
                            eventParticipants = eventParticipants,
                            eventLength = eventLengthInHours,
                            event = event,
                            recurringEventID = recurringEventID,
                            recurringEventStartDate = recurringEventStartDate,
                            recurringVolunteers = recurringVolunteers,
                            bannedUsers = bannedUsers,
                            trainedParticipantsList = trainedParticipantsList,
                            eventWaitlistData = eventWaitlistData,
                            currentRsvpAmount = currentRsvpAmount)



@admin_bp.route('/addVolunteersToEvent/<eventId>', methods = ['POST'])
def addVolunteer(eventId):
    event = Event.get_by_id(eventId)
    successfullyAddedVolunteer = False
    usernameList = []
    eventParticipants = getEventParticipants(eventId)
    usernameList = request.form.getlist("volunteer[]")

    successfullyAddedVolunteer = False
    for user in usernameList:
        userObj = User.get_by_id(user)
        successfullyAddedVolunteer = addPersonToEvent(userObj, event)
        if successfullyAddedVolunteer == "already in":
            flash(f"{userObj.fullName} already in table.", "warning")
        else:
            if successfullyAddedVolunteer:
                flash(f"{userObj.fullName} added successfully.", "success")
            else:
                flash(f"Error when adding {userObj.fullName} to event." ,"danger")

    if 'ajax' in request.form and request.form['ajax']:
        return ''

    return redirect(url_for('admin.trackVolunteersPage', eventID = eventId))

@admin_bp.route('/rsvpFromWaitlist/<username>/<eventId>', methods = ['POST'])
def rsvpFromWaitlist(username, eventId):
    if g.current_user.isAdmin: 
        (EventRsvp.update(rsvpWaitlist = False).where(EventRsvp.event_id == eventId, EventRsvp.user_id == username)).execute()
    return ""

@admin_bp.route('/addVolunteersToEvent/<username>/<eventId>/isBanned', methods = ['GET'])
def isVolunteerBanned(username, eventId):
    return {"banned":1} if isBannedFromEvent(username, eventId) else {"banned":0}

@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user==user, EventParticipant.event==eventID)).execute()
    (EventRsvp.delete().where(EventRsvp.user==user, EventRsvp.event==eventID)).execute()
    flash("Volunteer successfully removed", "success")
    return ""

@admin_bp.route('/addBackgroundCheck', methods = ['POST'])
def addBackgroundCheck():
    if g.current_user.isCeltsAdmin:
        eventData = request.form
        user = eventData['user']
        bgStatus = eventData['bgStatus']
        type = eventData['bgType']
        dateCompleted = eventData['bgDate']
        addUserBackgroundCheck(user, type, bgStatus, dateCompleted)
        return " "

@admin_bp.route('/deleteBackgroundCheck', methods = ['POST'])
def deleteBackgroundCheck():
    if g.current_user.isCeltsAdmin:
        eventData = request.form
        bgToDelete = BackgroundCheck.get_by_id(eventData['bgID'])
        BackgroundCheck.delete().where(BackgroundCheck.id == bgToDelete).execute()
        return ""

@admin_bp.route('/updateProgramManager', methods=["POST"])
def updateProgramManager():
    if g.current_user.isCeltsAdmin:
        data =request.form
        username = User.get(User.username == data["user_name"])
        program = Program.get_by_id(data['program_id'])
        setProgramManager(data["user_name"], data["program_id"], data["action"])
        createLog(f'{username.firstName} has been {data["action"]}ed as a Program Manager for {program.programName}')
        return ""
    else:
        abort(403)

@admin_bp.route("/updatePhone", methods=["POST"])
def updatePhone():
    newinfo=request.form
    User.update(phoneNumber=newinfo["phoneNumber"]).where(User.username==newinfo["username"]).execute()
    return ""

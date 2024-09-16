from flask import request, render_template, redirect, url_for, flash, abort, g, json, jsonify
from peewee import DoesNotExist, JOIN
from playhouse.shortcuts import model_to_dict
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.program import Program
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.emergencyContact import EmergencyContact
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateEventParticipants, getEventLengthInHours, addUserBackgroundCheck, setProgramManager
from app.logic.participants import trainedParticipants, addPersonToEvent, getParticipationStatusForTrainings, sortParticipantsByStatus
from app.logic.events import getPreviousRepeatingEventData, getEventRsvpCount
from app.models.eventRsvp import EventRsvp
from app.models.backgroundCheck import BackgroundCheck
from app.logic.createLogs import createActivityLog, createRsvpLog
from app.logic.users import getBannedUsers, isBannedFromEvent


@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def getVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    return json.dumps(searchUsers(query))

@admin_bp.route('/event/<eventID>/manage_volunteers', methods=['GET', 'POST'])
def manageVolunteersPage(eventID):
    """
    Controller that handles POST and GET requests regarding the Manage Volunteers page.

    POST: updates the event participants for a particular event by calling 
    updateEventParticipants on the form.

    GET: retrieves all necessary participant lists and dictionaries and categorizes
    the participants/volunteers into their respective participation statuses. Then 
    renders the manageVolunteers.html template.
    """
    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}", e)
        abort(404)

    # ------------ POST request ------------
    if request.method == "POST":
        volunteerUpdated = updateEventParticipants(request.form)

        # error handling depending on the boolean returned from updateEventParticipants
        if volunteerUpdated:
            flash("Volunteer table succesfully updated", "success")
        else:
            flash("Error adding volunteer", "danger")
        return redirect(url_for("admin.manageVolunteersPage", eventID=eventID))
    
    # ------------ GET request ------------
    elif request.method == "GET":
        if not (g.current_user.isCeltsAdmin or (g.current_user.isCeltsStudentStaff and g.current_user.isProgramManagerForEvent(event))):
            abort(403)

        # ------- Grab the different lists of participants -------
        trainedParticipantsForProgramAndTerm = trainedParticipants(event.program, event.term)

        bannedUsersForProgram = [bannedUser.user for bannedUser in getBannedUsers(event.program)]
  
        eventNonAttendedData, eventWaitlistData, eventVolunteerData, eventParticipants = sortParticipantsByStatus(event)
        
        allRelevantUsers = [participant.user for participant in (eventParticipants + eventNonAttendedData + eventWaitlistData)]
        
        # ----------- Get miscellaneous data -----------

        participationStatusForTrainings = getParticipationStatusForTrainings(event.program, allRelevantUsers, event.term)

        eventLengthInHours = getEventLengthInHours(event.timeStart, event.timeEnd, event.startDate)

        recurringVolunteers = getPreviousRepeatingEventData(event.recurringId)

        currentRsvpAmount = getEventRsvpCount(event.id)

        # ----------- Render template with all of the data ------------
        return render_template("/events/manageVolunteers.html",
                                eventVolunteerData = eventVolunteerData,
                                eventNonAttendedData = eventNonAttendedData,
                                eventWaitlistData = eventWaitlistData,
                                eventLength = eventLengthInHours,
                                event = event,
                                recurringVolunteers = recurringVolunteers,
                                bannedUsersForProgram = bannedUsersForProgram,
                                trainedParticipantsForProgramAndTerm = trainedParticipantsForProgramAndTerm,
                                participationStatusForTrainings = participationStatusForTrainings,
                                currentRsvpAmount = currentRsvpAmount)

@admin_bp.route('/event/<eventID>/volunteer_details', methods=['GET'])
def volunteerDetailsPage(eventID):
    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}", e)
        abort(404)

    if not (g.current_user.isCeltsAdmin or (g.current_user.isCeltsStudentStaff and g.current_user.isProgramManagerForEvent(event))):
        abort(403)

    eventRsvpData = list(EventRsvp.select(EmergencyContact, EventRsvp)
                                  .join(EmergencyContact, JOIN.LEFT_OUTER, on=(EmergencyContact.user==EventRsvp.user))
                                  .where(EventRsvp.event==event))
    eventParticipantData = list(EventParticipant.select(EmergencyContact, EventParticipant)
                                                .join(EmergencyContact, JOIN.LEFT_OUTER, on=(EmergencyContact.user==EventParticipant.user))
                                                .where(EventParticipant.event==event))
    
    waitlistUser = list(set([obj for obj in eventRsvpData if obj.rsvpWaitlist]))
    rsvpUser = list(set([obj for obj in eventRsvpData if not obj.rsvpWaitlist ]))

    return render_template("/events/volunteerDetails.html",
                            waitlistUser = waitlistUser,
                            attendedUser= eventParticipantData,
                            rsvpUser= rsvpUser,
                            event = event)


@admin_bp.route('/addVolunteersToEvent/<eventId>', methods = ['POST'])
def addVolunteer(eventId):
    event = Event.get_by_id(eventId)
    successfullyAddedVolunteer = False
    usernameList = request.form.getlist("selectedVolunteers[]")
    successfullyAddedVolunteer = False
    alreadyAddedList = []
    addedSuccessfullyList = []
    errorList = []
    
    for user in usernameList:
        userObj = User.get_by_id(user)
        successfullyAddedVolunteer = addPersonToEvent(userObj, event)
        if successfullyAddedVolunteer == "already in":
            alreadyAddedList.append(userObj.fullName)
        else:
            if successfullyAddedVolunteer:
                addedSuccessfullyList.append(userObj.fullName)
            else:
                errorList.append(userObj.fullName)

    volunteers = ""
    if alreadyAddedList:
        volunteers = ", ".join(vol for vol in alreadyAddedList)
        flash(f"{volunteers} was already added to this event.", "warning")

    if addedSuccessfullyList:
        volunteers = ", ".join(vol for vol in addedSuccessfullyList)
        flash(f"{volunteers} added successfully.", "success")
    
    if errorList:
        volunteers = ", ".join(vol for vol in errorList)
        flash(f"Error when adding {volunteers} to event.", "danger")

    if 'ajax' in request.form and request.form['ajax']:
        return ''

    return redirect(url_for('admin.manageVolunteersPage', eventID = eventId))

@admin_bp.route('/rsvpFromWaitlist/<username>/<eventId>', methods = ['POST'])
def rsvpFromWaitlist(username, eventId):
    event = Event.get_by_id(eventId)
    isProgramManager = g.current_user.isProgramManagerFor(event.program)
    if g.current_user.isCeltsAdmin or (g.current_user.isCeltsStudentStaff and isProgramManager): 
        waitlistUsers = EventRsvp.select(EventRsvp, User).join(User).where(EventRsvp.user == username, EventRsvp.event==eventId).execute()
        if (waitlistUsers):
            createRsvpLog(event.id, f"Moved {waitlistUsers[0].user.fullName} from waitlist to RSVP.")
            (EventRsvp.update(rsvpWaitlist = False).where(EventRsvp.event_id == eventId, EventRsvp.user_id == username)).execute()
    return ""

@admin_bp.route('/addVolunteersToEvent/<username>/<eventId>/isBanned', methods = ['GET'])
def isVolunteerBanned(username, eventId):
    return {"banned":1} if isBannedFromEvent(username, eventId) else {"banned":0}

@admin_bp.route('/removeVolunteerFromEvent', methods = ['POST'])
def removeVolunteerFromEvent():
    user = request.form.get('username')
    eventID = request.form.get('eventId')
    if g.current_user.isAdmin:
        userInRsvpTable = EventRsvp.select(EventRsvp, User).join(User).where(EventRsvp.user == user, EventRsvp.event==eventID).execute()
        if (userInRsvpTable):
            rsvpUser = userInRsvpTable[0]
            if rsvpUser.rsvpWaitlist:
                createRsvpLog(eventID, f"Removed {rsvpUser.user.fullName} from waitlist.")
            else:
                createRsvpLog(eventID, f"Removed {rsvpUser.user.fullName} from RSVP list.")
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
        createActivityLog(f'{username.firstName} has been {data["action"]}ed as a Program Manager for {program.programName}')
        return ""
    else:
        abort(403)

@admin_bp.route("/updatePhone", methods=["POST"])
def updatePhone():
    newinfo=request.form
    User.update(phoneNumber=newinfo["phoneNumber"]).where(User.username==newinfo["username"]).execute()
    return ""

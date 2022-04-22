from flask import request, render_template, redirect, url_for, request, flash, abort, g, json, jsonify
from datetime import datetime
from peewee import DoesNotExist

from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.matchParticipants import MatchParticipants
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateEventParticipants, addVolunteerToEventRsvp, getEventLengthInHours,setUserBackgroundCheck
from app.logic.participants import trainedParticipants, getEventParticipants,getOutsideParticipants
from app.models.user import User
from app.models.eventRsvp import EventRsvp
from app.models.backgroundCheck import BackgroundCheck



@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def getVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    return json.dumps(searchUsers(query,"volunteers"))

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
    outsideParticipants = getOutsideParticipants(event)
    if not g.current_user.isCeltsAdmin:
        abort(403)

    eventRsvpData = (EventRsvp
        .select()
        .where(EventRsvp.event==event))

    eventLengthInHours = getEventLengthInHours(
        event.timeStart,
        event.timeEnd,
        event.startDate)

    isPastEvent = (datetime.now() >= datetime.combine(event.startDate, event.timeStart))

    matched = MatchParticipants.select().where(MatchParticipants.event==event)
    matches = {} #This will contain the matches for a particular event

    for entry in matched:
        if entry.volunteer and entry.outsideParticipant:
            if entry.volunteer not in matches:
                matches[entry.volunteer]=[entry.outsideParticipant]
            else:
                matches[entry.volunteer].append(entry.outsideParticipant)

    return render_template("/events/trackVolunteers.html",
        eventRsvpData=list(eventRsvpData),
        eventParticipants=eventParticipants,
        eventLength=eventLengthInHours,
        program=program,
        event=event,
        isPastEvent=isPastEvent,
        trainedParticipantsList=trainedParticipantsList,
        outsideParticipants = outsideParticipants,
        matches = matches)

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

@admin_bp.route('/addVolunteerToEvent', methods = ['POST'])
def addVolunteer():
    volunteerData = request.form
    username = volunteerData["username"]
    user = User.get(User.username==username)
    eventId = volunteerData['eventId'][0]
    successfullyAddedVolunteer = addVolunteerToEventRsvp(user, eventId)
    EventParticipant.create(user=user, event=eventId) # user is present
    if successfullyAddedVolunteer:
        flash("Volunteer successfully added!", "success")
    else:
        flash("Error when adding vol    unteer", "danger")
    return ""

@admin_bp.route('/addOutsideParticipantToEvent', methods = ['POST'])
def addOutsideParticipant():

    outsideParticipantData = request.form
    email = outsideParticipantData['email']
    eventId = outsideParticipantData['eventId']
    event = eventId.split(':')
    newEntry = MatchParticipants.get_or_create(outsideParticipant=email,event=int(event[0]))
    if newEntry[-1]==False:
        flash("Participant already added to this event!", "danger")
    else:
        flash("Participant succesfully added to the event!", "success")
    return ""

@admin_bp.route('/matchParticipants', methods = ['POST'])
def matchParticipant():
    matchData = request.form

    volunteer = matchData['volunteer']
    outsideParticipant = matchData['outsideParticipant']
    eventId = matchData['eventId'][0]

    vol = User.get_by_id(volunteer)
    update = MatchParticipants.get_or_none(MatchParticipants.outsideParticipant==outsideParticipant,MatchParticipants.event==int(eventId),MatchParticipants.volunteer==None)
    if update != None:
        update.volunteer = volunteer
        update.save()
        flash("Participant succesfully matched to volunteer", "success")

    else:
        flash("Participant already matched to someone", "danger")
    return ""


@admin_bp.route('/unMatch', methods = ['POST'])
def unMatch():
    matchData = request.form

    volunteer = matchData['volunteer']
    outsideParticipant = matchData['outsideParticipant']
    eventId = matchData['eventId'][0]

    volunteer = User.get_by_id(volunteer)
    query = MatchParticipants.get(MatchParticipants.volunteer==volunteer,MatchParticipants.outsideParticipant==outsideParticipant,MatchParticipants.event==eventId)
    query.volunteer = None
    query.save()
    flash("Outside particpant successfully removed", "success")
    return ""

@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user==user, EventParticipant.event==eventID)).execute()
    (EventRsvp.delete().where(EventRsvp.user==user)).execute()
    update = (MatchParticipants.update({MatchParticipants.volunteer: None}).where(MatchParticipants.volunteer==user,MatchParticipants.event==eventID))
    update.execute()

    flash("Volunteer successfully removed", "success")
    return ""

@admin_bp.route('/removeOutsideParticipantFromEvent/<outsideParticipant>/<eventID>', methods = ['POST'])
def removeParticipantFromEvent(outsideParticipant, eventID):
    (MatchParticipants.delete().where(MatchParticipants.outsideParticipant==outsideParticipant, MatchParticipants.event==eventID)).execute()
    flash("Particpant successfully removed", "success")
    return ""

@admin_bp.route('/updateBackgroundCheck', methods = ['POST'])
def updateBackgroundCheck():
    if g.current_user.isCeltsAdmin:
        eventData = request.form
        user = eventData['user']
        checkPassed = int(eventData['checkPassed'])
        type = eventData['bgType']
        setUserBackgroundCheck(user,type, checkPassed)
        return " "

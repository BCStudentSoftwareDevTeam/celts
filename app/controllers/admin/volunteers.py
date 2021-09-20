from flask import request, render_template, redirect, url_for, request, flash
from peewee import DoesNotExist

from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateVolunteers, addVolunteerToEvent
from app.models.user import User
from flask import json, jsonify

@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def getVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    return json.dumps(searchUsers(query))

@admin_bp.route('/event/<eventID>/track_volunteers', methods=['GET'])
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

    attendedTraining = trainedParticipants(program)
    if g.current_user.isCeltsAdmin:
        eventParticipantsData = EventParticipant.select().where(EventParticipant.event == event)
        eventParticipantsData = eventParticipantsData.objects()
        eventLengthInHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)

        return render_template("/events/trackVolunteers.html",
                                eventParticipantsData = list(eventParticipantsData),
                                eventLength = eventLengthInHours,
                                program = program,
                                event = event,
                                attendedTraining=attendedTraining)
    else:
        abort(403)


@admin_bp.route('/event/<eventID>/track_volunteers', methods=['POST'])
def updateVolunteerTable(programID, eventID):

    try:
        event = Event.get_by_id(eventID)
    except DoesNotExist as e:
        print(f"No event found for {eventID}")
        abort(404)

    program = event.singleProgram
    # TODO: What do we do for no programs or multiple programs?
    if not program:
        return "TODO: What do we do for no programs or multiple programs?"


    volunteerUpdated = updateVolunteers(request.form)
    if volunteerUpdated:
        flash("Volunteer table succesfully updated")
    else:
        flash("Error adding volunteer")

    return redirect(url_for("admin.trackVolunteersPage", eventID=eventID))


@admin_bp.route('/addVolunteerToEvent/<volunteer>/<volunteerEventID>/<eventLengthInHours>', methods = ['POST'])
def addVolunteer(volunteer, volunteerEventID, eventLengthInHours):
    volunteer = volunteer.strip("()")
    username = volunteer.split('(')[-1]
    user = User.get(User.username == username)
    succesfullyAddedVolunteer = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    if succesfullyAddedVolunteer:
        flash("Volunteer successfully added!", "success")
    else:
        flash("Error when adding volunteer", "danger")
    return "" #must return something for ajax



@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == eventID)).execute()
    flash("Volunteer successfully removed")
    return "Volunteer successfully removed"

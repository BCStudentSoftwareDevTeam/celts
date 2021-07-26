from flask import request, render_template, redirect, url_for, request, flash
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchVolunteers import searchVolunteers
from app.logic.updateTrackHours import updateTrackHours
from app.models.user import User
from peewee import *

@admin_bp.route('/searchTrackHoursVolunteers/<query>', methods = ['GET'])
def searchTrackHoursVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    try:
        return searchVolunteers(query)

    except Exception as e:
        return e, 500


@admin_bp.route('/<programID>/<eventID>/track_hours', methods=['POST'])
def updateHours(programID, eventID):
    updateTrackHoursMsg = updateTrackHours(request.form)
    if updateTrackHoursMsg == None:
        flash("Volunteer table succesfully updated")
        return redirect(url_for("admin.trackVolunteerHoursPage", programID=programID, eventID=eventID))
    else:
        flash("Error adding volunteer")
        return redirect(url_for("admin.trackVolunteerHoursPage", programID=programID, eventID=eventID))


@admin_bp.route('/addVolunteerToEvent/<user>/<volunteerEventID>/<eventLengthInHours>', methods = ['POST'])
def addVolunteerToEvent(user, volunteerEventID, eventLengthInHours):
    '''
    Adds a volunteer to the eventparticipant table database after a search and click to 'Add participant' button
    param: user- string containing first name, last name, and username (format: "<firstName> <lastName> (<username>)")
           volunteerEventID - id of the event the volunteer is being registered for
           eventLengthInHours - how long the event lasts (how may hours to give the student) (type: float)
    '''
    try:
        user = user.strip("()")
        userName=user.split('(')[-1]

        alreadyVolunteered = (EventParticipant.select().where(EventParticipant.user==userName, EventParticipant.event==volunteerEventID)).exists()
        if alreadyVolunteered:
            flash("Volunteer already exists.", "warning")
            return "Volunteer already exists."

        else:
            EventParticipant.create(user=userName, event = volunteerEventID, attended = True, hoursEarned = eventLengthInHours)
            flash("Volunteer successfully added!", "success")
            return "Volunteer successfully added!"

    except Exception as e:
        flash("Error when adding volunteer", "danger")
        return "Error when adding volunteer", 500


@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == eventID)).execute()
    flash("Volunteer successfully removed")
    return "Volunteer successfully removed"

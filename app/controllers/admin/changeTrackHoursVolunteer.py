from flask import request, render_template, redirect, url_for, request, flash
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchVolunteers import searchVolunteers
from app.logic.updateTrackHours import updateTrackHours, addVolunteerToEvent
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
def addVolunteer(user, volunteerEventID, eventLengthInHours):
    succesfullyAddedVolunteer = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    if succesfullyAddedVolunteer:
        flash("Volunteer successfully added!", "success")
    else:
        flash("Error when adding volunteer", "danger")
    return ""




@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == eventID)).execute()
    flash("Volunteer successfully removed")
    return "Volunteer successfully removed"

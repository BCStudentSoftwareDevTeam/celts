from flask import request, render_template, redirect, url_for, request, flash
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.searchVolunteers import searchVolunteers
from app.logic.updateVolunteers import updateVolunteers, addVolunteerToEvent
from app.models.user import User
from peewee import *

@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def getVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    return searchVolunteers(query)



@admin_bp.route('/<programID>/<eventID>/track_volunteers', methods=['POST'])
def updateVolunteerTable(programID, eventID):

    volunteerUpdated = updateVolunteers(request.form)
    if volunteerUpdated:
        flash("Volunteer table succesfully updated")
    else:
        flash("Error adding volunteer")

    return redirect(url_for("admin.trackVolunteersPage", programID=programID, eventID=eventID))


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

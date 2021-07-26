from flask import request, render_template, redirect, url_for, request, flash
from flask import json, jsonify
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from peewee import *

@admin_bp.route('/searchTrackHoursVolunteers/<query>', methods = ['GET'])
def searchTrackHoursVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    try:
        query = query.strip()
        search = query.upper()
        splitSearch = search.split()
        resultsDict = {}

        firstName = splitSearch[0] + "%"
        lastName = " ".join(splitSearch[1:]) +"%"

        if len(splitSearch) == 1: #search for first or last name
            results = User.select().where(User.isStudent & User.firstName ** firstName | User.lastName ** firstName)
            for participant in results:
                if participant not in resultsDict:
                    resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"
        else:
            for searchTerm in splitSearch: #searching for specified first and last name
                if len(searchTerm) > 1:
                    searchTerm += "%"
                    results = User.select().where(User.isStudent & User.firstName ** firstName & User.lastName ** lastName)
                    for participant in results:
                        if participant not in resultsDict:
                            resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"

        dictToJSON = json.dumps(resultsDict)
        return dictToJSON

    except Exception as e:
        return e, 500


@admin_bp.route('/removeVolunteerFromEvent/<user>/<eventID>', methods = ['POST'])
def removeVolunteerFromEvent(user, eventID):
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == eventID)).execute()
    flash("Volunteer successfully removed")
    return "Volunteer successfully removed"

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
        search = query.upper() + "%"

        results = User.select().where(User.isStudent & User.firstName ** search | User.lastName ** search)
        resultsDict = {}
        for participant in results:
            resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"
            # resultsDict[participant.firstName + " " + participant.lastName+ "("+ participant.username +")"] = participant.firstName + " " + participant.lastName+" ("+participant.username+")"
        dictToJSON = json.dumps(resultsDict)
        return dictToJSON
    except Exception as e:
        return "Error Searching Volunteers query", 500

from flask import request, render_template, redirect, url_for
from flask import json, jsonify
from app.controllers.admin import admin_bp
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from peewee import *


@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():

    return render_template('addParticipants.html',
                            title="Add Participants")

@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def searchVolunteers(query):

    try:
        query = query.strip()
        search = query.upper() + "%"
        results = User.select().where(User.firstName ** search | User.lastName ** search)
        resultsDict = {}
        for participant in results:
            resultsDict[participant.firstName + " " + participant.lastName] = participant.firstName + " " + participant.lastName
        dictToJSON = json.dumps(resultsDict)
        return dictToJSON
    except Exception as e:
        print(e)
        return "Error Searching Volunteers query", 500

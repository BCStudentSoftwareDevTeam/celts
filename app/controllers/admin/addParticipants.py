from flask import request, render_template
from flask import json, jsonify
from app.controllers.admin import admin_bp
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from peewee import *

@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():
    outsideParticipants = OutsideParticipant.select(
                                                    OutsideParticipant.firstName,
                                                    OutsideParticipant.lastName,
                                                    OutsideParticipant.email,
                                                    OutsideParticipant.phoneNumber)

    eventParticipants = (User.select(User.firstName, User.lastName, User.bnumber)
                                        .join(EventParticipant, on = (User.username == EventParticipant.user_id)))

    return render_template('addParticipants.html',
                            title="Add Participants",
                            outsideParticipants = outsideParticipants,
                            eventParticipants = eventParticipants)

@admin_bp.route("/createParticipant", methods = ['POST'])
def createParticipant():
    try:
        rsp = (request.data).decode("utf-8")
        rspFunctional = json.loads(rsp);
        participantData = [
            {
                "event": 2,
                "email": rspFunctional["emailEntry"],
                "firstName": rspFunctional["firstName"],
                "lastName": rspFunctional["lastName"],
                "phoneNumber": rspFunctional["phoneNumber"]
            }
        ]
        OutsideParticipant.insert_many(participantData).on_conflict_replace().execute()
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return "Error Updating Participant Data", 500

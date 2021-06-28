from flask import request, render_template
from flask import json, jsonify
from app.controllers.admin import admin_bp
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.user import User

@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():
    outsideParticipants = OutsideParticipant.select(
                                                    OutsideParticipant.firstName,
                                                    OutsideParticipant.lastName,
                                                    OutsideParticipant.email,
                                                    OutsideParticipant.phoneNumber)
    eventParticipants = (User.select(User.firstName, User.lastName, User.bnumber)
                                        .join(EventParticipant, on = (User.username == EventParticipant.user_id)))
    # outsidePartList = []
    # outsidePartList.append(outsideParticipants)
    return render_template('addParticipants.html',
                            title="Add Participants",
                            outsideParticipants = outsideParticipants,
                            eventParticipants = eventParticipants)

@admin_bp.route('/createParticipant', methods = ['POST'])
def createParticipant():
    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    try:
        newOutsideParticipant = [
            {
                # "event": 1,
                "firstName": firstName,
                "lastName": lastName,
                "email": email,
                "phoneNumber": phone
            }
        ]
        OutsideParticipant.insert_many(newOutsideParticipant).on_conflict_replace().execute()

    except:
        return "", 500
    return ""

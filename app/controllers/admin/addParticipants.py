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
    # outsidePartList = []
    # outsidePartList.append(outsideParticipants)
    return render_template('addParticipants.html',
                            title="Add Participants",
                            outsideParticipants = outsideParticipants,
                            eventParticipants = eventParticipants)

@admin_bp.route("/createParticipant", methods = ['POST'])
def createParticipant():  # firstName, lastName, email, phoneNumber):
    print("\nLOOK HERE "*5)
    # print(request.data)
    rsp = (request.data)  #.decode("utf-8")  # This turns byte data into a string
    # print(rsp)
    rspFunctional = json.loads(rsp)
    print(rspFunctional)
    # try:
    # emailEntry = "" #FIXME
    op = OutsideParticipant.insert(OutsideParticipant.event_id == event, OutsideParticipant.email == emailEntry).on_conflict_replace().execute()
                                        # OutsideParticipant.firstName == firstName,
                                        # OutsideParticipant.lastName == lastName,
                                        # OutsideParticipant.email == email,
                                        # OutsideParticipant.phoneNumber == phoneNumber))
    op.firstName = firstName, op.lastName = lastName

    # except:
        # return "", 500
    return " "

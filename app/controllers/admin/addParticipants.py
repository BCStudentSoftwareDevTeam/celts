from flask import request, render_template, redirect, url_for
from flask import json, jsonify
from app.controllers.admin import admin_bp
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from peewee import *

@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():
    partDict = {}
    outsideParticipants = OutsideParticipant.select(
                                                    OutsideParticipant.firstName,
                                                    OutsideParticipant.lastName,
                                                    OutsideParticipant.email,
                                                    OutsideParticipant.phoneNumber)

    eventParticipants = (User.select(User.firstName, User.lastName, User.bnumber)
                                        .join(EventParticipant, on = (User.username == EventParticipant.user_id)))

    for participant in outsideParticipants:
        username = participant.email.split("@")[0].lstrip()
        partDict[username] = []
        for i in (participant.firstName, participant.lastName, participant.phoneNumber, participant.email):
            partDict[username].append(i)
    print(partDict)

    return render_template('addParticipants.html',
                            title="Add Participants",
                            outsideParticipants = outsideParticipants,
                            eventParticipants = eventParticipants)

# @admin_bp.route("/removeParticipant", methods = ['POST'])
# def removeParticipant():
#     try:
#         # print(request.data)
#         rsp = (request.data).decode("utf-8")
#         rspFunctional = json.loads(rsp);
#         # print(rspFunctional*5)
#         participantData = [
#             {
#                 "event": 2,
#                 "email": rspFunctional["emailEntry"],
#             }
#         ]
#         removeData = OutsideParticipant.select().where(OutsideParticipant.email==rspFunctional["emailEntry"])
#         removeData.delete_instance()
#         return jsonify(success=True)
#     except Exception as e:
#         print(e)
#         return "Error Removing Participant Data", 500

# @admin_bp.route("/createParticipant", methods = ['POST'])
# def createParticipant():
#
#         OutsideParticipant.get_or_create(
#                                         event_id= 2,
#                                         firstName= request.form['firstNameTextarea'],
#                                         lastName= request.form['lastNameTextarea'],
#                                         email= request.form['emailTextarea'],
#                                         phoneNumber= request.form['phoneNumberTextarea'])
#         # return redirect("/addParticipants")
#         return "Successfully added"

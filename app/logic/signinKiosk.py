
from flask import Flask
from app.models.eventParticipant import EventParticipant
from app.models.user import User

def sendkioskData(bnumber, eventid):
"""Accepts scan input and signs in the user. If user exists or is already
signed in will return flasher"""
    bNumberToUsername = User.select().where(User.bnumber == bnumber).objects()[0]
    attendedParticipants = (EventParticipant.select(EventParticipant.user)
                                            .where(EventParticipant.attended, EventParticipant.event == eventid))

    attendedList = [participant.user for participant in attendedParticipants ]

    if bNumberToUsername not in attendedList:
        (EventParticipant.update({EventParticipant.attended: True})
                         .where(EventParticipant.user == bNumberToUsername, EventParticipant.event == eventid)).execute()
        alreadySignedIn = False
    else:
        alreadySignedIn = True
    return bNumberToUsername, alreadySignedIn

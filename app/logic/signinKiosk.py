
from flask import Flask
from app.models.eventParticipant import EventParticipant
from app.models.user import User

def sendUserData(bnumber, eventid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return flasher"""
    bNumberToUser = User.get(User.bnumber == bnumber)
    if ((EventParticipant.select(EventParticipant.user)
                                            .join(User)
                                            .where(EventParticipant.attended, User.bnumber == bnumber, EventParticipant.event == eventid))
                                            .exists()):
        alreadySignedIn = True
    else:
        (EventParticipant.update({EventParticipant.attended: True})
                         .where(EventParticipant.user == bNumberToUser, EventParticipant.event == eventid)).execute()
        alreadySignedIn = False
    return bNumberToUser, alreadySignedIn

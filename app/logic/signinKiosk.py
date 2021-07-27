
from flask import Flask
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programBan import ProgramBan
from app.logic.programEligibility import isEligibleForProgram

def sendUserData(bnumber, eventid, programid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return flasher"""
    bNumberToUser = User.get(User.bnumber == bnumber)
    if not isEligibleForProgram(programid, bNumberToUser):
        userStatus = "banned"
    elif ((EventParticipant.select(EventParticipant.user)
                         .join(User)
                         .where(EventParticipant.attended, User.bnumber == bnumber, EventParticipant.event == eventid))
                         .exists()):
        userStatus = "already in"
    else:
        (EventParticipant.update({EventParticipant.attended: True})
                         .where(EventParticipant.user == bNumberToUser, EventParticipant.event == eventid)).execute()
        userStatus = "success"
    return bNumberToUser, userStatus

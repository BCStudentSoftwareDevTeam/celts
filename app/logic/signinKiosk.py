
from flask import Flask
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programBan import ProgramBan
from app.logic.programEligibility import isEligibleForProgram

def sendUserData(bnumber, eventid, programid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return flasher"""
    bNumberToUser = User.get(User.bnumber == bnumber)
    if (ProgramBan.select().where(ProgramBan.user == bNumberToUser)) and (ProgramBan.select().where(ProgramBan.program == programid)):
        userStatus = "banned"
        print(f"{bNumberToUser.username.upper()} IS BANNED")
    elif ((EventParticipant.select(EventParticipant.user)
                         .join(User)
                         .where(EventParticipant.attended, User.bnumber == bnumber, EventParticipant.event == eventid))
                         .exists()):
        userStatus = "already in"
        print("ALREADY IN")
    else:
        (EventParticipant.update({EventParticipant.attended: True})
                         .where(EventParticipant.user == bNumberToUser, EventParticipant.event == eventid)).execute()
        userStatus = "success"
        print("SUCCESS")
    return bNumberToUser, userStatus

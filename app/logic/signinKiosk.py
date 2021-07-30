
from flask import Flask
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programBan import ProgramBan
from app.logic.programEligibility import isEligibleForProgram

def sendUserData(bnumber, eventid, programid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return user and login status"""
    signInUser = User.get(User.bnumber == bnumber)
    if not isEligibleForProgram(programid, signInUser):
        userStatus = "banned"
    elif ((EventParticipant.select(EventParticipant.user)
                           .where(EventParticipant.attended, EventParticipant.user == signInUser, EventParticipant.event == eventid))
                           .exists()):
        userStatus = "already in"
    else:
        userStatus = "success"
        if EventParticipant.get_or_none(EventParticipant.user == signInUser, EventParticipant.event == eventid):
            (EventParticipant.update({EventParticipant.attended: True})
                             .where(EventParticipant.user == signInUser, EventParticipant.event == eventid)).execute()
        else:
            EventParticipant.insert([{EventParticipant.user: signInUser,
                                      EventParticipant.event: eventid,
                                      EventParticipant.rsvp: False,
                                      EventParticipant.attended: True,
                                      EventParticipant.hoursEarned: 0}]).execute()
    return bNumberToUser, userStatus

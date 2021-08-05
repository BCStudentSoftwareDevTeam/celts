from app.models.event import Event
from flask import Flask
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.logic.updateVolunteers import getEventLengthInHours
from app.models.programBan import ProgramBan
from app.logic.programEligibility import isEligibleForProgram

def sendUserData(bnumber, eventid, programid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return user and login status"""
    signInUser = User.get(User.bnumber == bnumber)
    event = Event.get_by_id(eventid)
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
            totalHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)
            EventParticipant.insert([{EventParticipant.user: signInUser,
                                      EventParticipant.event: eventid,
                                      EventParticipant.rsvp: False,
                                      EventParticipant.attended: True,
                                      EventParticipant.hoursEarned: totalHours}]).execute()
    return signInUser, userStatus

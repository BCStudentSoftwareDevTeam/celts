from app.models import*
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.controllers.events.meetsReqsForEvent import isEligibleForProgram
# from app.controllers.
import pytest

#Fixme: Import meetReqforEvent
#meetReqForEvent = False
#meetReq = meetReqForEvent
def volunteerRegister(userid,  eventid):

    user = User.get(User.username == userid)
    event = Event.get(Event.id == eventid)
    #Assuming the student meets the requirement for the events (function wriiten by Zach and KArina)

    if isEligibleForProgram(event, user):
        eventParticipant = EventParticipant.get(EventParticipant.user == user, EventParticipant.event == event, EventParticipant.rsvp == True)
        return eventParticipant
    else:
        return ("User is not eligible for the program")

from app.models import*
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
import pytest

#Fixme: Import meetReqforEvent
#meetReqForEvent = False
#meetReq = meetReqForEvent
def volunteerRegister(userid,  eventid):

    user = User.get(User.username == userid)
    event = Event.get(Event.id == eventid)
    #Assuming the student meets the requirement for the events (function wriiten by Zach and KArina)

    eventParticipant = EventParticipant.create(user = user, event = event, rsvp = True)
    return eventParticipant

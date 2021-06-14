from app.models import*
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
import pytest

#Fixme: Import meetReqforEvent
meetReqForEvent = False
def volunteerRegister(user:User, event:Event):
    #Assuming the student meets the requirement for the events (function wriiten by Zach and KArina)
    if meetReqForEvent:
        eventParticipant = EventParticipant.create(user = user, event = event, rsvp = True)
        return eventParticipant
    else:
        raise ValueError()

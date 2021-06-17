from app.models import*
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.controllers.events.meetsReqsForEvent import isEligibleForProgram
import pytest

def volunteerRegister(userid,  eventid):

    user = User.get(User.username == userid)
    event = Event.get(Event.id == eventid)
    # Assuming the student meets the requirement for the events (function wriiten by Zach and KArina)

    if isEligibleForProgram(event, user):
        if EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event == event) is None:
            eventParticipant = EventParticipant.create(user = user, event = event, rsvp = True)
        else:
            return f"{user} is already registered for {event}"
        return eventParticipant
    else:
        return ("User is not eligible for the program")

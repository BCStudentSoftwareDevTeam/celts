from app.models import*
from app.models.event import Event
from app.models.program import Program
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.controllers.events.programEligibility import isEligibleForProgram
import pytest

def userRsvpForEvent(userid,  eventid):
    """
    Lets the user RSVP for an event if they are eligible and create an entry for them is in the EventParticipant table
    :param userid: accepts a User object or a username of a user
    :param eventid: accepts an Event object or a valid eventid
    :return: eventParticipant entry for the given user and event; otherwise raise an exception
    """
    print("forever")
    user = User.get(User.username == userid)
    print(eventid,"line19")
    event = Event.get(Event.id == eventid)
    program = Event.select(Event.program).where(Event.id == event)

    if isEligibleForProgram(program, user):
        #checks if user isn't already registerd for event
        eventParticipant, newParticipant = EventParticipant.get_or_create(user = user,
                                                       event = event,
                                                       rsvp = True)
        return eventParticipant

    raise Exception("User is not eligible")

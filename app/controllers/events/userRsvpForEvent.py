from app.models import*
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.controllers.events.programEligibility import isEligibleForProgram
import pytest

def userRsvpForEvent(userid,  eventid):
    """
    Lets the user RSVP for an event if they are eligible and create an entry for them is in the EventParticipant table
    :param userid: it is the username of a user
    :param eventid: an integer
    :return: eventParticipant entry for that user; otherwise raise an exception error
    """

    user = User.get(User.username == userid)
    event = Event.get(Event.id == eventid)
    program = Event.select(Event.program).where(Event.id == event)

    try:
        if isEligibleForProgram(program, user):
        #checks if user isn't already registerd for event
            eventParticipant = EventParticipant.get_or_create(user = user,
                                                       event = event,
                                                       rsvp = True)
            return eventParticipant
    except Exception as err:

        raise ("User is not eligible", err)

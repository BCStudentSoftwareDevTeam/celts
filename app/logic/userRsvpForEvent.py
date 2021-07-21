from app.models import*
from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.logic.programEligibility import isEligibleForProgram
import pytest

def userRsvpForEvent(user,  event):
    """
    Lets the user RSVP for an event if they are eligible and creates an entry for them in the EventParticipant table.

    :param user: accepts a User object or username
    :param event: accepts an Event object or a valid event ID
    :return: eventParticipant entry for the given user and event; otherwise raise an exception
    """

    user = User.get_by_id(user)
    event = Event.get_by_id(event)
    program = Program.select(Program).join(ProgramEvent).where(ProgramEvent.event == event).get()
    EventParticipant.get_or_create(user = user, event = event, rsvp = True)[0]

    if isEligibleForProgram(program, user):
        return True

    else:
        return False
    # raise Exception("User is not eligible")

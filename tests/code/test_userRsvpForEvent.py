import pytest
from app.models.user import User
from app.controllers.events.userRsvpForEvent import userRsvpForEvent
from app.models.event import Event
from peewee import DoesNotExist
from app.controllers.events.programEligibility import isEligibleForProgram

@pytest.mark.integration
def test_notUserRsvpForEvent():

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("asdkl", 1)

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent(132546, 1)

@pytest.mark.integration
def test_noEventUserRsvpForEvent():

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", 1500)

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", "Event")

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", -1)

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", 0)


@pytest.mark.integration
def test_userRsvpForEvent():

    volunteer = userRsvpForEvent("lamichhanes2", 10)

    assert volunteer.user.username == "lamichhanes2"
    assert volunteer.event.id == 10
    assert volunteer.rsvp == True

    # the user has already registered for the event
    volunteer = userRsvpForEvent("lamichhanes2", 10)
    assert volunteer.event.id == 10
    assert volunteer

    # the user is not eligible to register (reason: hasn't attended all prerequisite events)
    with pytest.raises(Exception):
        volunteer = userRsvpForEvent("ayisie", 7)

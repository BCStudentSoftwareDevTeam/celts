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

    assert volunteer[0].user.username == "lamichhanes2"
    assert volunteer[0].event.id == 10
    assert volunteer[0].rsvp == True

    # the user has already registered for the event
    volunteer2 = userRsvpForEvent("lamichhanes2", 10)

    assert volunteer2

    # the user is not eligible to register (reason: hasn't attended all prerequisite events)
    volunteer3 = userRsvpForEvent("ayisie", 7)
    assert volunteer3 == None

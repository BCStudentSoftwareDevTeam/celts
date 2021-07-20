import pytest
from app.models.user import User
from app.logic.userRsvpForEvent import userRsvpForEvent
from app.models.event import Event
from peewee import DoesNotExist
from app.logic.programEligibility import isEligibleForProgram

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

    volunteer = userRsvpForEvent("agliullovak", 12)
    assert volunteer.user.username == "agliullovak"
    assert volunteer.event.id == 12
    assert volunteer.rsvp == True

    # the user has already registered for the event
    volunteer = userRsvpForEvent("agliullovak", 12)
    assert volunteer.event.id == 12
    assert volunteer

    # the user is not eligible to register (reason: hasn't attended all prerequisite events)
    with pytest.raises(Exception):
        volunteer = userRsvpForEvent("ayisie", 7)

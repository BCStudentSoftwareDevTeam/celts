import pytest
from app.models.eventParticipant import EventParticipant
from app.controllers.events.volunteerRegisterEvent import volunteerRegister
from peewee import DoesNotExist
from app.models.user import User
from app.models.event import Event
from app.controllers.events.meetsReqsForEvent import isEligibleForProgram

@pytest.mark.integration
def test_noUserVolunteerRegister():

    user = User.get(User.username == "asdlkfje")
    program = Event.get(Event.id == 1)
    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(program, "lamichhanes2")

    user = User.get(User.username == 123156)
    program = Event.get(Event.id == 1)
    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(program, 135156)

    user = User.get(User.username == "khatts")
    program = Event.get(Event.id == 1)
    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(program, user)

    user = User.get(User.username == "khatts")
    program = Event.get(Event.id == 1)
    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(program, user)


@pytest.mark.integration
def test_volunteerEligible():

    user = User.get(User.username == "lamichhanes2")
    program = Event.get(Event.id == 1)
    attended = EventParticipant.get(EventParticipant.attended == 1)

    eligible = isEligibleForProgram(program, user)

    assert eligible

import pytest
from peewee import DoesNotExist
from app.models.user import User
from app.models.event import Event
from app.controllers.events.meetsReqsForEvent import isEligibleForProgram

# @pytest.mark.integration
# def test_noUserVolunteerRegister():

    # user = User.get(User.username == "asdlkfje")
    # event = Event.get(Event.id == 1)
    # with pytest.raises(DoesNotExist):
    #     eligible = isEligibleForProgram(event, "lamichhanes2")

    # user = User.get(User.username == 123156)
    # event = Event.get(Event.id == 1)
    # with pytest.raises(DoesNotExist):
    #     eligible = isEligibleForProgram(event, 135156)
    #
    # user = User.get(User.username == "khatts")
    # event = Event.get(Event.id == 1)
    # with pytest.raises(DoesNotExist):
    #     eligible = isEligibleForProgram(event, user)
    #
    # user = User.get(User.username == "khatts")
    # event = Event.get(Event.id == 1)
    # with pytest.raises(DoesNotExist):
    #     eligible = isEligibleForProgram(event, user)


@pytest.mark.integration
def test_volunteerEligible():

    user = User.get(User.username == "lamichhanes2")
    event = Event.get(Event.id == 2)

    eligible = isEligibleForProgram(event, user)
    assert eligible

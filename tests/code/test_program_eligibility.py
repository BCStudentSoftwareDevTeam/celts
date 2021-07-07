import pytest
from app.models.eventParticipant import EventParticipant
from app.controllers.events.volunteerRegisterEvent import volunteerRegister
from peewee import DoesNotExist
from app.models.user import User
from app.models.event import Event
from app.controllers.events.programEligibility import isEligibleForProgram
from app.models.program import Program
@pytest.mark.integration
def test_noUserVolunteerRegister():

    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(2, "asdlkfje") #user doesn't exist

    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(2, 135156)

    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(9, "lamichhanes2") #Program doesn't exist



@pytest.mark.integration
def test_volunteerEligible():

    user = User.get(User.username == "lamichhanes2")
    program = Program.get(Program.id == 2)
    attended = EventParticipant.get(EventParticipant.attended == 1)

    eligible = isEligibleForProgram(program, user)

    assert eligible

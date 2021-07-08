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

    eligible = isEligibleForProgram(program, user)

    assert eligible

    user2 = User.get(User.username == "khatts") #user that is banned from a program
    program2 = Program.get(Program.id == 1)


    eligible2 = isEligibleForProgram(program2, user2)

    assert eligible2 == False

    # user haven't attend the required event
    user3 = User.get(User.username == "ayisie")
    program3 = Program.get(Program.id == 1)

    eligible3 = isEligibleForProgram(program3, user3)
    print(eligible3)

    assert eligible3 == False

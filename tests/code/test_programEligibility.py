import pytest
from app.models.eventParticipant import EventParticipant
from peewee import DoesNotExist

from app.models.program import Program
from app.models.user import User
from app.models.event import Event
from app.logic.programEligibility import isEligibleForProgram

@pytest.mark.integration
def test_doesNotExistIsEligibleForProgram():

    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(2, "asdlkfje") #user doesn't exist

    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(2, 135156)

    with pytest.raises(DoesNotExist):
        eligible = isEligibleForProgram(9, "lamichhanes2") #Program doesn't exist



@pytest.mark.integration
def test_isEligibleForProgram():

    # user has attended all required events
    user = User.get(User.username == "lamichhanes2")
    program = Program.get(Program.id == 2)

    eligible = isEligibleForProgram(2, "lamichhanes2")
    assert eligible
    eligible = isEligibleForProgram(program, user)
    assert eligible

    # there are no required events
    eligible = isEligibleForProgram(4, "ayisie")
    assert eligible

    # user that is banned from a program
    eligible = isEligibleForProgram(3,  "khatts")
    assert not eligible

    # user hasn't attend the required event
    eligible3 = isEligibleForProgram(1, "ayisie")
    assert not eligible3

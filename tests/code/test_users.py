import pytest
from peewee import IntegrityError, DoesNotExist

from app.models.program import Program
from app.models.user import User
from app.logic.users import addRemoveInterest
from app.logic.users import isEligibleForProgram

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

@pytest.mark.integration
def test_addRemoveInterest():
    user = "ramsayb2"
    program_id = 1

    # test adding and removing test cases for different users
    rule = 'addInterest'
    result = addRemoveInterest(rule, program_id, user)
    assert result == "Successfully added interest"

    rule = 'deleteInterest'
    result = addRemoveInterest(rule, program_id, user)
    assert result == 'Successfully removed interest'

    rule = 'addInterest'
    user = "khatts"
    result = addRemoveInterest(rule, program_id, user)
    assert result == 'Successfully added interest'

    # test add and removing interest with different program id
    rule = 'addInterest'
    program_id = 3
    result = addRemoveInterest(rule, program_id, user)
    assert result == 'Successfully added interest'

    rule = 'deleteInterest'
    result = addRemoveInterest(rule, program_id, user)
    assert result == 'Successfully removed interest'

@pytest.mark.integration
def test_addRemoveInvalidInterest():

    program_id = 3

    #test for user that doesn't exist
    user = "al;skfjelh"
    rule = 'addInterest'
    with pytest.raises(IntegrityError):
        result = addRemoveInterest(rule, program_id, user)
        result == "Successfully added interest"

    #test removing interest that doesn't exist
    user = "lamichhanes2"
    rule = 'deleteInterest'
    program_id = 1
    result = addRemoveInterest(rule, program_id, user)
    assert result == "This interest does not exist"

    # test for incorrect rule
    rule = "lkejfiv"
    result = addRemoveInterest(rule, program_id, user)
    assert result == None

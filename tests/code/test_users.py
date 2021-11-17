import pytest
from peewee import IntegrityError, DoesNotExist

from app.models.program import Program
from app.models.user import User
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram
from app.logic.users import isEligibleForProgram

@pytest.mark.integration
def test_user_model():
    user = User.get_by_id("ramsayb2")
    assert user.isCeltsAdmin
    assert not user.isCeltsStudentStaff
    assert user.isAdmin

    user = User.get_by_id("partont")
    assert not user.isCeltsAdmin
    assert not user.isCeltsStudentStaff
    assert not user.isAdmin

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
def test_addUserInterest():
    username = "ramsayb2"
    program_id = 2

    # test adding interest for different users
    result = addUserInterest(program_id, username)
    assert result == "Successfully added interest"


    username = "khatts"
    result = addUserInterest(program_id, username)
    assert result == 'Successfully added interest'

    # test adding interest with different program id
    program_id = 3
    result = addUserInterest(program_id, username)
    assert result == 'Successfully added interest'



# @pytest.mark.integration
# def test_addRemoveInvalidInterest():
#
#     program_id = 3
#
#     #test for user that doesn't exist
#     user = "al;skfjelh"
#     rule = 'addInterest'
#     with pytest.raises(IntegrityError):
#         result = addRemoveInterest(rule, program_id, user)
#         result == "Successfully added interest"
#
#     #test removing interest that doesn't exist
#     user = "lamichhanes2"
#     rule = 'deleteInterest'
#     program_id = 1
#     result = addRemoveInterest(rule, program_id, user)
#     assert result == "This interest does not exist"
#
#     # test for incorrect rule
#     rule = "lkejfiv"
#     result = addRemoveInterest(rule, program_id, user)
#     assert result == None

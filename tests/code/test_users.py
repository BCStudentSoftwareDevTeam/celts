import pytest
from app.models.program import Program
from app.models.note import Note
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

    # test adding interest for user that does not exist
    username = "jarjug"
    program_id = 3
    with pytest.raises(AssertionError):
        result = addUserInterest(program_id, username)
        assert result == 'Successfully added interest'

    # test adding interest for program_id that does not exist
    username = "khatts"
    program_id = 45
    with pytest.raises(AssertionError):
        result = addUserInterest(program_id, username)
        assert result == 'Successfully added interest'





@pytest.mark.integration
def test_removeUserInterestt():

    #test for removing interest
    username = "ramsayb2"
    program_id = 2
    result = removeUserInterest(program_id, username)
    assert result == "Successfully removed interest"

    username = "khatts"
    program_id = 2
    result = removeUserInterest(program_id, username)
    assert result == "Successfully removed interest"

    #test removing interest with different program id
    program_id = 3
    result = removeUserInterest(program_id, username)
    assert result == "Successfully removed interest"

    # test adding interest for user that does not exist
    username = "jarjug"
    program_id = 3
    with pytest.raises(AssertionError):
        result = addUserInterest(program_id, username)
        assert result == 'Successfully added interest'

    # test adding interest for program_id that does not exist
    username = "khatts"
    program_id = 45
    with pytest.raises(AssertionError):
        result = addUserInterest(program_id, username)
        assert result == 'Successfully added interest'


@pytest.mark.integration
def test_banUser():

    #test for banning a user from a program
    username = "khatts"
    program_id = 2
    note = "Banning user test"
    creator = "ramsayb2"
    banEndDate = "2022-11-29"
    status = banUser (program_id, username, note, banEndDate, creator)
    assert status == "Successfully banned the user"

    #test for banning a user from a program with different program is
    program_id = 3
    status = banUser (program_id, username, note, banEndDate, creator)
    assert status == "Successfully banned the user"



@pytest.mark.integration
def test_unbanUser():

    #test for banning a user from a program
    username = "khatts"
    program_id = 2
    note = "unbanning user test"
    creator = "ramsayb2"
    status = unbanUser (program_id, username, note, creator)
    assert status == "Successfully unbanned the user"

    #test for banning a user from a program with different program is
    program_id = 3
    status = unbanUser (program_id, username, note, creator)
    assert status == "Successfully unbanned the user"

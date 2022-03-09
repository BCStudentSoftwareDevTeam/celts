import pytest
from peewee import *
from datetime import datetime
from app.models import mainDB
from app.models.program import Program
from app.models.note import Note
from app.models.user import User
from app.models.programBan import ProgramBan
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
    assert result


    username = "khatts"
    result = addUserInterest(program_id, username)
    assert result

    # test adding interest with different program id
    program_id = 3
    result = addUserInterest(program_id, username)
    assert result

    # test adding interest for user that does not exist
    username = "jarjug"
    program_id = 3
    with pytest.raises(IntegrityError):
        result = addUserInterest(program_id, username)
        assert result

    # test adding interest for program_id that does not exist
    username = "khatts"
    program_id = 45
    with pytest.raises(IntegrityError):
        result = addUserInterest(program_id, username)
        assert result





@pytest.mark.integration
def test_removeUserInterestt():

    #test for removing interest
    username = "ramsayb2"
    program_id = 2
    result = removeUserInterest(program_id, username)
    assert result ==  True

    username = "khatts"
    program_id = 2
    result = removeUserInterest(program_id, username)
    assert result == True

    #test removing interest with different program id
    program_id = 3
    result = removeUserInterest(program_id, username)
    assert result == True

    # test adding interest for user that does not exist
    username = "jarjug"
    program_id = 3
    with pytest.raises(IntegrityError):
        result = addUserInterest(program_id, username)
        assert result == True

    # test adding interest for program_id that does not exist
    username = "khatts"
    program_id = 45
    with pytest.raises(IntegrityError):
        result = addUserInterest(program_id, username)
        assert result == True


@pytest.mark.integration
def test_banUser():
    with mainDB.atomic() as transaction:
        #test for banning a user from a program
        username = "khatts"
        programId = 2
        note = "Banning user test"
        creator = "ramsayb2"
        banEndDate = "2022-11-29"
        banUser (programId, username, note, banEndDate, creator)

        banned = ProgramBan.get(ProgramBan.program==programId)
        assert banned.user.username == username
        assert banned.endDate == datetime.strptime(banEndDate, '%Y-%m-%d').date()
        assert banned.banNote.noteContent == note
        assert banned.banNote.createdBy.username == creator

        #test for banning a user from a program with different program id
        programId = 5
        banUser (programId, username, note, banEndDate, creator)
        banned = ProgramBan.get(ProgramBan.program==programId)
        assert banned.user.username == username
        assert banned.endDate == datetime.strptime(banEndDate, '%Y-%m-%d').date()
        assert banned.banNote.noteContent == note
        assert banned.banNote.createdBy.username == creator

        transaction.rollback()

@pytest.mark.integration
def test_unbanUser():
    with mainDB.atomic() as transaction:
        #test for unbanning a user from a program
        username = "khatts"
        programId = 2
        creator = "ramsayb2"

        banNote = "Banning user test"
        banEndDate = "2022-11-29"
        banUser (programId, username, banNote, banEndDate, creator)

        unbanNote = "unbanning user test"
        unbanUser (programId, username, unbanNote, creator)
        unbanned = ProgramBan.get(ProgramBan.program==programId)
        assert unbanned.user.username == username
        assert unbanned.endDate == datetime.now().date()
        assert unbanned.unbanNote.noteContent == unbanNote
        assert unbanned.unbanNote.createdBy.username == creator

        #test for unbanning a user from a program with different program
        programId = 3
        banUser (programId, username, banNote, banEndDate, creator)
        unbanUser (programId, username, unbanNote, creator)
        unbanned = ProgramBan.get(ProgramBan.program==programId)
        assert unbanned.user.username == username
        assert unbanned.endDate == datetime.now().date()
        assert unbanned.unbanNote.noteContent == unbanNote
        assert unbanned.unbanNote.createdBy.username == creator

        transaction.rollback()

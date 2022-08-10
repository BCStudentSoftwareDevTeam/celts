import pytest
from peewee import *
from datetime import datetime
from app.models import mainDB
from app.models.program import Program
from app.models.programBan import ProgramBan
from app.models.note import Note
from app.models.user import User
from app.models.programManager import ProgramManager
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram
from app.logic.users import isEligibleForProgram

@pytest.mark.integration
def test_user_model():

    user = User.get_by_id("ramsayb2")
    assert user.isCeltsAdmin
    assert not user.isCeltsStudentStaff
    assert user.isAdmin
    assert user.fullName == "Brian Ramsay"

    user = User.get_by_id("partont")
    assert not user.isCeltsAdmin
    assert not user.isCeltsStudentStaff
    assert not user.isAdmin
    assert user.fullName == "Tyler Parton"

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
    with mainDB.atomic() as transaction:

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

        transaction.rollback()

@pytest.mark.integration
def test_removeUserInterestt():
    with mainDB.atomic() as transaction:
        #test for removing interest that exists
        username = "ramsayb2"
        program_id = 2
        result = removeUserInterest(program_id, username)
        assert result ==  True

        #test for removing interest that doesn't exist
        username = "khatts"
        program_id = 2
        result = removeUserInterest(program_id, username)
        assert result == True

        transaction.rollback()

@pytest.mark.integration
def test_banUser():
    with mainDB.atomic() as transaction:

        #test for banning a user from a program
        username = User.get_by_id("khatts")
        program_id = 2
        note = "Banning user test"
        creator = "ramsayb2"
        banEndDate = "2022-11-29"
        banUser(program_id, username, note, banEndDate, creator)
        prg2BannedUsers = list(User.select().join(ProgramBan).where(ProgramBan.program == program_id))
        assert username in prg2BannedUsers

        #test for exceptions when banning the user
        username = "khatts"
        program_id = 100
        note = "Banning user test"
        creator = "ramsayb2"
        banEndDate = "2022-11-29"
        with pytest.raises(Exception):
            status = banUser (program_id, username, note, banEndDate, creator)
            assert status == False

        transaction.rollback()

@pytest.mark.integration
def test_unbanUser():
    with mainDB.atomic() as transaction:

        #test for unbanning a user from a program
        username = User.get_by_id("khatts")
        program_id = 2
        note = "unbanning user test"
        creator = "ramsayb2"
        unbanUser(program_id, username, note, creator)
        prg2BannedUsers = list(User.select().join(ProgramBan).where(ProgramBan.program == program_id))
        assert username not in prg2BannedUsers

        #test for exceptions when unbanning the user
        username = "ramsayb2"
        program_id = 100
        note = "Banning user test"
        creator = "ramsayb2"
        banEndDate = "2022-11-29"
        with pytest.raises(Exception):
            status = unbanUser (program_id, username, note, creator)
            assert status == False

        transaction.rollback()

@pytest.mark.integration
def test_userpriv():

    user = User.get_by_id("khatts")
    prg = Program.get_by_id(1)
    assert user.isProgramManagerFor(prg)

    user = User.get_by_id("mupotsal")
    prg = Program.get_by_id(10)
    assert not user.isProgramManagerFor(prg)

@pytest.mark.integration
def test_Add_Remove_ProgramManager():
    with mainDB.atomic() as transaction:

        # See if the user is being added as a Program Manager
        user = User.get_by_id("mupotsal")
        prg = Program.get_by_id(1)
        newPM = user.addProgramManager(prg)
        PMsWithNewPM = list(User.select().join(ProgramManager).where(ProgramManager.program_id == 1))

        # Make sure what is expected is returned
        assert newPM == (f' {user} added as Program Manager')
        # Check that the user is made manager of program 1
        assert user in PMsWithNewPM

        # See if the user is being removed from being a Program Manager
        removePM = user.removeProgramManager(prg)
        noPM = list(User.select().join(ProgramManager).where(ProgramManager.program_id == 1))

        # Make sure what is expected is returned
        assert removePM == (f'{user} removed from Program Manager')
        # Check that the Program Manager is actually removed from the Program Manager table
        assert user not in noPM

        transaction.rollback()

@pytest.mark.integration
def test_getStudentManagerForEvent():
    with mainDB.atomic() as transaction:

        #Test data for creating a program
        testProgramData = [
        {
        "id":13,
        "programName":"testProgram",
        "isStudentLed": False,
        "isBonnerScholars":False,
        }
        ]

        #Inserts new row into Program table
        Program.insert_many(testProgramData).on_conflict_replace().execute()

        #Test data for creating an event
        testEvent = [
        {
        "id": 16,
        "term": 2,
        "name": "testEvent",
        "description": "testEvent",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Seabury Center",
        "startDate": datetime.strptime("2021 10 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
        }
        ]

        Event.insert_many(testEvent).on_conflict_replace().execute() #Inserts new row into Event table

        #Test data for creating a new row in ProgramEvent table
        testProgramEvent = [
        {
        "program_id":13,
        "event_id":16,
        }
        ]

        #Inserts new row into ProgramEvent table
        ProgramEvent.insert_many(testProgramEvent).on_conflict_replace().execute()

        #Test data for test users, inserted in User table
        testUserData = [
        {#This user is not a program manager
        "username": "testUser",
        "bnumber": "B00724094",
        "email": "martinj2@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Joey",
        "lastName": "Martin",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False

        },
        {#This user is a program manager
        "username": "testUser2",
        "bnumber": "B00762158",
        "email": "studentmanagertest@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Paw",
        "lastName": "Thaw",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": True
        }
        ]

        #Insert new row into User table
        User.insert_many(testUserData).on_conflict_replace().execute()

        #Test data for StudentManager table, inserted in to StudentManager table
        testProgramManagerData = [
        {
        'user': 'testUser2',
        'program': 13
        }
        ]

        #Insert new row into StudentManager table
        ProgramManager.insert_many(testProgramManagerData).on_conflict_replace().execute()

        test_program = 13 #programID is passed in  as an int
        test_event = Event.get_by_id(16) #gets event object
        student = User.get_by_id("testUser") #This test user is not a program manager
        programManager = User.get_by_id("testUser2") ##This user is a program manager

        ## user is manager of program
        assert programManager.isProgramManagerForEvent(test_event) == True
        ## user is not manager of program
        assert student.isProgramManagerForEvent(test_event) == False

        transaction.rollback()

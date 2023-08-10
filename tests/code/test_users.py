import pytest
from peewee import *
from datetime import datetime
from dateutil import parser
from app import app
from flask import g

from app.models import mainDB
from app.models.program import Program
from app.models.programBan import ProgramBan
from app.models.note import Note
from app.models.profileNote import ProfileNote
from app.models.user import User
from app.models.programManager import ProgramManager
from app.models.backgroundCheck import BackgroundCheck
from app.models.event import Event
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram, getUserBGCheckHistory, addProfileNote, deleteProfileNote, getBannedUsers, isBannedFromEvent, updateDietInfo
from app.logic.volunteers import addUserBackgroundCheck

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
def test_addUserProfileNote():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = "ramsayb2"
            profileNote = addProfileNote(1, True, "Test profile note", "neillz")
            assert profileNote == ProfileNote.get_by_id(profileNote.id)

            profileNote2 = addProfileNote(3, False, "Test profile note 2", "ramsayb2")
            assert profileNote2 == ProfileNote.get_by_id(profileNote2.id)
            assert profileNote2.viewTier == 3

            profileNote3 = addProfileNote(3, True, "Test profile note 3", "ramsayb2")
            assert profileNote3 == ProfileNote.get_by_id(profileNote3.id)
            assert profileNote3.viewTier == 1
        transaction.rollback()

@pytest.mark.integration
def test_deleteUserProfileNote():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = "ramsayb2"

            addedNote = addProfileNote(1, True, "Test profile note", "neillz")
            assert addedNote.isBonnerNote == True
            assert addedNote.viewTier == 1
            assert addedNote.user == User.get_by_id("neillz")

            profileNote = deleteProfileNote(addedNote)
            with pytest.raises(DoesNotExist):
                ProfileNote.get_by_id(addedNote)

            addedNote = addProfileNote(3, False, "Test profile note 2", "ramsayb2")
            profileNote = deleteProfileNote(addedNote)
            with pytest.raises(DoesNotExist):
                ProfileNote.get_by_id(addedNote.id)

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
    assert user.isProgramManagerFor(prg), "khatts should be program manager"

    # Test the case where we use the same object and want to calculate for a different program
    prg = Program.get_by_id(10)
    assert not user.isProgramManagerFor(prg), "khatts should not be program manager"

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
        "id": 17,
        "term": 2,
        "name": "testEvent",
        "description": "testEvent",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Seabury Center",
        "startDate": datetime.strptime("2021 10 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "program": 9
        }
        ]

        Event.insert_many(testEvent).on_conflict_replace().execute() #Inserts new row into Event table

        #Inserts new row into Event table
        Event.update(program_id=13).where(Event.id == 16).execute()

        # This user will not be a program manager
        testUserData = [
        {
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
        # This user will be a program manager
        {
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

        # Insert new rows into User table
        User.insert_many(testUserData).on_conflict_replace().execute()

        # Insert new row into StudentManager table
        ProgramManager.create(user='testUser2',program=13)

        test_event = Event.get_by_id(16) #gets event object
        student = User.get_by_id("testUser") #This test user is not a program manager
        programManager = User.get_by_id("testUser2") ##This user is a program manager

        # user is manager of program
        assert programManager.isProgramManagerForEvent(test_event) == True

        # user is not manager of program
        assert student.isProgramManagerForEvent(test_event) == False

        transaction.rollback()

@pytest.mark.integration
def test_getUserBGCheckHistory():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = "ramsayb2"

            # Create a test user to run background checks on
            testusr = User.create(username = 'usrtst',
                                  firstName = 'Test',
                                  lastName = 'User',
                                  bnumber = '03522492',
                                  email = 'usert@berea.deu',
                                  isStudent = True)

            # Add background checks to the user
            addUserBackgroundCheck("usrtst","CAN", "Submitted", parser.parse("2020-9-20"))
            addUserBackgroundCheck("usrtst","SHS", "Submitted", parser.parse("2020-10-20"))
            testusrHistory = getUserBGCheckHistory(testusr)
            # Check that all the users background checks have been submitted and
            # they are returned correctly. Also make sure that the background check
            # that has not been given anything is returend as empty
            assert "Submitted" == testusrHistory['CAN'][0].backgroundCheckStatus
            assert "Submitted" == testusrHistory['SHS'][0].backgroundCheckStatus
            assert [] == testusrHistory['FBI']
            assert [] == testusrHistory['BSL']

            # Update one of the background Checks and make sure that the updated
            # check is returned and the original check is still returned as well
            addUserBackgroundCheck("usrtst","SHS", "Passed", parser.parse("2020-12-20"))
            testusrHistory = getUserBGCheckHistory(testusr)
            assert "Passed" == testusrHistory['SHS'][0].backgroundCheckStatus
            assert "Submitted" == testusrHistory['SHS'][1].backgroundCheckStatus
            assert "Submitted" == testusrHistory['CAN'][0].backgroundCheckStatus
            assert [] == testusrHistory['FBI']
            assert [] == testusrHistory['BSL']

        transaction.rollback()

@pytest.mark.integration
def test_getBannedUsers():
    with mainDB.atomic() as transaction:
        userToBan = User.create(username = 'usrtst', # Test banned user
                              firstName = 'Test',
                              lastName = 'User',
                              bnumber = '03522492',
                              email = 'usert@berea.deu',
                              isStudent = True)
        banUser(1, User.get_by_id("usrtst"), "nope", "2050-11-29", "ramsayb2")
        assert userToBan in [user.user for user in getBannedUsers(1)]

        unbanUser(1, User.get_by_id("usrtst"), "yep", "ramsayb2")  # Test eligible but previously banned user
        assert userToBan not in [user.user for user in getBannedUsers(1)]

        notBannedUser = User.create(username = 'usrtst2', # Test eligible user
                              firstName = 'Test',
                              lastName = 'User 2',
                              bnumber = '03522493',
                              email = 'usert2@berea.deu',
                              isStudent = True)
        assert notBannedUser not in [user.user for user in getBannedUsers(1)]
        transaction.rollback()

@pytest.mark.integration
def test_isBannedFromEvent():
    with mainDB.atomic() as transaction:
        userToBan = User.create(username = 'usrtst', # Test banned user
                              firstName = 'Test',
                              lastName = 'User',
                              bnumber = '03522492',
                              email = 'usert@berea.deu',
                              isStudent = True)
        banUser(1, User.get_by_id("usrtst"), "nope", "2050-11-29", "ramsayb2")
        assert isBannedFromEvent("usrtst", 1)

        unbanUser(1, 'usrtst', "yep", "ramsayb2") # Test eligible but previously banned user
        assert not isBannedFromEvent("usrtst", 1)

        notBannedUser = User.create(username = 'usrtst2', # Test eligible user
                              firstName = 'Test',
                              lastName = 'User 2',
                              bnumber = '03522493',
                              email = 'usert2@berea.deu',
                              isStudent = True)
        assert not isBannedFromEvent("usrtst2", 1)
        transaction.rollback()

@pytest.mark.integration
def test_updateDietInfo():
    with mainDB.atomic() as transaction:

        updateDietInfo("khatts", "Cheese")
        diet = User.select().where(User.username == "khatts")
        content = [list.dietRestriction for list in diet]
        assert content == ["Cheese"]

        updateDietInfo("khatts", "Beef")
        newDiet = User.select().where(User.username == "khatts")
        newContent = [list.dietRestriction for list in newDiet]
        assert newContent == ["Beef"]

    transaction.rollback()

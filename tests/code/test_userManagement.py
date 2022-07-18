import pytest
from flask import g
from app import app
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.logic.volunteers import setProgramManager
from peewee import DoesNotExist
from app.models import mainDB

@pytest.mark.integration
def test_modifyCeltsAdmin():
    user = "agliullovak"
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsAdmin == False
    with app.app_context():
        g.current_user = "ramsayb2"
        addCeltsAdmin(userInTest)
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsAdmin == True
        removeCeltsAdmin(userInTest)
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsAdmin == False

        with pytest.raises(DoesNotExist):
            addCeltsAdmin("blahbah")
        with pytest.raises(DoesNotExist):
            addCeltsAdmin("ksgvoidsid;")

def test_modifyCeltsStudentStaff():
    user = "mupotsal"
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsAdmin == False
    with app.app_context():
        g.current_user = "ramsayb2"
        addCeltsStudentStaff(userInTest)
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsStudentStaff == True
    with app.app_context():
        g.current_user = "ramsayb2"
        removeCeltsStudentStaff(userInTest)
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsStudentStaff == False
    with app.app_context():
        g.current_user = "ramsayb2"
        with pytest.raises(DoesNotExist):
            addCeltsStudentStaff("asdf")
        with pytest.raises(DoesNotExist):
            removeCeltsStudentStaff("1234")

@pytest.mark.integration
def test_changeProgramInfo():
    with mainDB.atomic() as transaction:
        programId = 3
        emailSenderName = "New Test Name"
        emailReplyTo = 'newtest@email'
        currentProgramInfo = Program.get_by_id(programId)
        assert currentProgramInfo.emailSenderName == "testName"
        assert currentProgramInfo.emailReplyTo == "test@email"
        changeProgramInfo(emailReplyTo, emailSenderName, programId)
        currentProgramInfo = Program.select().where(Program.id==programId).get()
        assert currentProgramInfo.emailSenderName == emailSenderName
        assert currentProgramInfo.emailReplyTo == emailReplyTo
        transaction.rollback()

@pytest.mark.integration
def test_updatedProgramManager():

    #checking if the user is being updated when added to programs
    user_name = "mupotsal"
    program_id = 1
    action = "add"
    setProgramManager(user_name, program_id, action)
    assert ProgramManager.get_or_none(ProgramManager.program == program_id, ProgramManager.user == user_name) is not None


    # Not a student staff, should not be added as a program manager
    user_name2 = "ramsayb2"
    program_id2 = 1
    action2 = "add"
    setProgramManager(user_name2, program_id2, action2)
    assert ProgramManager.get_or_none(ProgramManager.program==program_id2, ProgramManager.user == user_name2) is None

    # if action remove, user should be removed from the table
    user_name3 = "mupotsal"
    program_id3 = 1
    action3 = "remove"
    setProgramManager(user_name3, program_id3, action3)
    assert ProgramManager.get_or_none(ProgramManager.program==program_id3, ProgramManager.user == user_name3) is None

@pytest.mark.integration
def test_getAllowedPrograms():
    with mainDB.atomic() as transaction:
        # checks the length of all programs an admin has access to and compares that to total programs
        allowedPrograms = len(getAllowedPrograms(User.get_by_id("ramsayb2")))
        totalPrograms = Program.select().count()
        assert allowedPrograms == totalPrograms

        # creates program manager and checks the programs they can access
        User.create(username = "bledsoef",
                    bnumber = "B00775205",
                    email = "bledsoef@berea.edu",
                    phoneNumber = "(859)876-5309",
                    firstName = "Fips",
                    lastName = "Bledsoe",
                    isStudent = True,
                    isFaculty = False,
                    isStaff = False,
                    isCeltsAdmin = False,
                    isCeltsStudentStaff = True)

        ProgramManager.create(user = "bledsoef",
                              program = Program.get_by_id(3))
        ProgramManager.create(user = "bledsoef",
                              program = Program.get_by_id(6))
        ProgramManager.create(user = "bledsoef",
                              program = Program.get_by_id(5))

        allowedPrograms = len(getAllowedPrograms(User.get_by_id("bledsoef")))
        assert allowedPrograms == 3

        # checks to make sure users can't access any programs
        allowedPrograms = len(getAllowedPrograms(User.get_by_id("partont")))
        assert allowedPrograms == 0
        transaction.rollback()


@pytest.mark.integration
def test_getAllowedTemplates():
    # admin template check
    allowedTemplates = len(getAllowedTemplates(User.get_by_id("ramsayb2")))
    assert allowedTemplates == EventTemplate.select().where(EventTemplate.isVisible==True).count()

    # other user template check, should always be 0
    allowedTemplates = len(getAllowedTemplates(User.get_by_id("ayisie")))
    assert allowedTemplates == 0

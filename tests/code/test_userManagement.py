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

@pytest.mark.integration
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
        eventName = "Test Event Name"
        emailSenderName = "New Test Name"
        emailReplyTo = 'newtest@email'
        currentProgramInfo = Program.get_by_id(programId)

        assert currentProgramInfo.programName == "Adopt A Grandparent"
        assert currentProgramInfo.emailSenderName == "testName"
        assert currentProgramInfo.emailReplyTo == "test@email"

        changeProgramInfo(eventName, emailReplyTo, emailSenderName, programId)
        currentProgramInfo = Program.select().where(Program.id==programId).get()

        assert currentProgramInfo.programName == eventName
        assert currentProgramInfo.emailSenderName == emailSenderName
        assert currentProgramInfo.emailReplyTo == emailReplyTo

        transaction.rollback()

@pytest.mark.integration
def test_updatedProgramManager():
    with mainDB.atomic() as transaction:
        # Try to add a student who isnt Student Staff into a Program Manager: They should not be added.
        user = User.get_by_id("mupotsal")
        user.isCeltsStudentStaff = False
        user.save()
        program = Program.get_by_id(1)

        setProgramManager(user, program, "add")
        assert ProgramManager.get_or_none(program = program, user = user) is None

        # Make the previous student into a Student Staff then try to make them
        # a Program Manager again: They should be added to Program Managers.
        user.isCeltsStudentStaff = True
        user.save()

        setProgramManager(user, program, "add")
        assert ProgramManager.get_or_none(program = program, user = user) is not None

        # Remove the user that was added as a Program Manager
        setProgramManager(user, program, "remove")
        assert ProgramManager.get_or_none(program = program, user = user) is None

        transaction.rollback()

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

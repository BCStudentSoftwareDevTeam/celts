import pytest
import io
from flask import g
from app import app
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.logic.volunteers import setProgramManager
from peewee import DoesNotExist
from app.models import mainDB
import os
import time
from werkzeug.datastructures import FileStorage

@pytest.mark.integration
def test_modifyCeltsAdmin():
    with mainDB.atomic() as transaction:

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

        transaction.rollback()

@pytest.mark.integration
def test_modifyCeltsStudentStaff():
    with mainDB.atomic() as transaction:

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

        with app.app_context():
            g.current_user = "ramsayb2"

            user = "neillz"
            userInTest = User.get(User.username == user)
            assert userInTest.isCeltsStudentStaff
            userManagedPrograms = list([obj.program.programName for obj in ProgramManager.select(Program)
                             .join(Program).where(ProgramManager.user == userInTest)])
            assert len(userManagedPrograms) == 2

            removeCeltsStudentStaff(userInTest)
            
            userInTest = User.get(User.username == user)
            assert not userInTest.isCeltsStudentStaff
            userManagedPrograms = list([obj.program.programName for obj in ProgramManager.select(Program)
                             .join(Program).where(ProgramManager.user == userInTest)])
            assert len(userManagedPrograms) == 0

        transaction.rollback()


@pytest.mark.integration
def test_changeProgramInfo():
    with mainDB.atomic() as transaction:
        baseProgramData = {
            "programName" : "Test Program Name",
            "programDescription" : "This is the original test description",
            "partner" : "Original Test Partner",
            "contactName" : "",
            "contactEmail" : '',
            "location" : "",
            "instagramUrl" : "",
            "bereaUrl" : "",
            "facebookUrl" : ""
        }

        desiredProgramData = {
            "programName" : "Test Program Name",
            "programDescription" : "This is a test Description",
            "partner" : "Test Partner",
            "contactName" : "New Test Name",
            "contactEmail" : 'newtest@email',
            "location" : "Danforth Tech",
            "instagramUrl" : "www.instagram.com",
            "bereaUrl" : "www.berea.edu",
            "facebookUrl" : "www.facebook.com"
        }
        newProgram = Program.create(**baseProgramData)

        currentProgramInfo = Program.get_by_id(newProgram.id)
        currentProgramID = currentProgramInfo.id

        AttachmentUpload.create(program=currentProgramID, fileName=f'{currentProgramID}.jpg')

        assert currentProgramInfo.programName == desiredProgramData["programName"]
        assert currentProgramInfo.programDescription != desiredProgramData['programDescription']
        assert currentProgramInfo.partner != desiredProgramData['partner']
        assert currentProgramInfo.contactName == ""
        assert currentProgramInfo.contactEmail == ""
        assert currentProgramInfo.defaultLocation == ""
        assert currentProgramInfo.instagramUrl != None
        assert currentProgramInfo.bereaUrl != None
        assert currentProgramInfo.facebookUrl != None
       

        with app.test_request_context():
            g.current_user = "ramsayb2"
            changeProgramInfo(currentProgramID, None, **desiredProgramData)

        currentProgramInfo = Program.select().where(Program.id==currentProgramID).get()
        
        assert currentProgramInfo.programName == desiredProgramData["programName"]
        assert currentProgramInfo.programDescription == desiredProgramData["programDescription"]
        assert currentProgramInfo.partner == desiredProgramData["partner"]
        assert currentProgramInfo.contactName == desiredProgramData["contactName"]
        assert currentProgramInfo.contactEmail == desiredProgramData["contactEmail"]
        assert currentProgramInfo.defaultLocation == desiredProgramData["location"]
        assert currentProgramInfo.instagramUrl == desiredProgramData["instagramUrl"]
        assert currentProgramInfo.facebookUrl == desiredProgramData["facebookUrl"]
        assert currentProgramInfo.bereaUrl == desiredProgramData["bereaUrl"]

        transaction.rollback()

@pytest.mark.integration
def test_updatedProgramManager():
    with mainDB.atomic() as transaction:
        # Make student a program manager.
        nonStudentorStaffUser = User.create(username = "prospectiveProgramManager",
                                     bnumber = "B00000000003",
                                     email = "test@test.com",
                                     phoneNumber = "000-000-0000",
                                     firstName = "prosp",
                                     lastName = "ect",
                                     isStudent = False,
                                     isFaculty = False,
                                     isStaff = False,
                                     isCeltsAdmin = False,
                                     isCeltsStudentStaff = False)
                                     
        studentUser = User.create(username = "secondProspectiveProgramManager",
                                     bnumber = "B00000000023",
                                     email = "test@test.com",
                                     phoneNumber = "000-000-0000",
                                     firstName = "prosp",
                                     lastName = "ect",
                                     isStudent = True,
                                     isFaculty = False,
                                     isStaff = False,
                                     isCeltsAdmin = False,
                                     isCeltsStudentStaff = False)

        facultyUser = User.create(username = "thirdProspectiveProgramManager",
                                     bnumber = "B00000000033",
                                     email = "test@test.com",
                                     phoneNumber = "000-000-0000",
                                     firstName = "prosp",
                                     lastName = "ect",
                                     isStudent = False,
                                     isFaculty = True,
                                     isStaff = False,
                                     isCeltsAdmin = False,
                                     isCeltsStudentStaff = False)

        program = Program.get_by_id(1)
        setProgramManager(nonStudentorStaffUser, program, "add")
        setProgramManager(studentUser, program, "add")
        setProgramManager(facultyUser, program, "add")
        assert ProgramManager.get_or_none(program = program, user = nonStudentorStaffUser) is not None
        assert ProgramManager.get_or_none(program = program, user = studentUser) is not None
        assert ProgramManager.get_or_none(program = program, user = facultyUser) is not None

        # Remove the user that was added as a Program Manager
        setProgramManager(nonStudentorStaffUser, program, "remove")
        setProgramManager(studentUser, program, "remove")
        setProgramManager(facultyUser, program, "remove")
        assert ProgramManager.get_or_none(program = program, user = nonStudentorStaffUser) is None
        assert ProgramManager.get_or_none(program = program, user = studentUser) is None
        assert ProgramManager.get_or_none(program = program, user = facultyUser) is None
    
        transaction.rollback()

@pytest.mark.integration
def test_getAllowedPrograms():
    with mainDB.atomic() as transaction:
        # checks the length of all programs an admin has access to and compares that to total programs
        allowedPrograms = len(getAllowedPrograms(User.get_by_id("ramsayb2")))
        totalPrograms = Program.select().count()
        assert allowedPrograms == totalPrograms

        # creates program manager and checks the programs they can access
        User.create(username = "bledsoefd",
                    bnumber = "B00775205",
                    email = "bledsoefd@berea.edu",
                    phoneNumber = "(859)876-5309",
                    firstName = "Fips",
                    lastName = "Bledsoe",
                    isStudent = True,
                    isFaculty = False,
                    isStaff = False,
                    isCeltsAdmin = False,
                    isCeltsStudentStaff = True)

        ProgramManager.create(user = "bledsoefd",
                              program = Program.get_by_id(3))
        ProgramManager.create(user = "bledsoefd",
                              program = Program.get_by_id(6))
        ProgramManager.create(user = "bledsoefd",
                              program = Program.get_by_id(5))

        allowedPrograms = len(getAllowedPrograms(User.get_by_id("bledsoefd")))
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

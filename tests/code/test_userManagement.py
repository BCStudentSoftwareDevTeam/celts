import pytest
from flask import g
from app import app
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.logic.volunteers import setProgramManager
from app.models import mainDB

@pytest.mark.integration
def test_modifyCeltsAdmin():
    """
    A function that tests the addCeltsAdmin and removeCeltsAdmin functions. 
    
    Testing steps:

    1. Create two new users: a user that is a student staff and one that is faculty.
    2. Verify that both new user can be added as an admin.
    3. Make sure errors gets thrown when we try to add each of the users again.
    4. Verify that the users we just added can be removed successfully.
    5. Create a new user that is a student not a student staff.
    6. Make sure an error gets thrown when we add a user that is not a student staff.
    7. Make sure an error gets thrown when we try to add users that don't exist.
    8. Rollback changes.
    """
    with mainDB.atomic() as transaction:

        # Testing step 1
        testAdminCreationUser1 = User.create(username = "testAdminCreationUser1",
                                            bnumber = "B98736789",
                                            email = "testAdminCreationUser1@berea.edu",
                                            phoneNumber = "(859)876-5309",
                                            firstName = "Test",
                                            lastName = "AdminCreation",
                                            isStudent = True,
                                            isFaculty = False,
                                            isStaff = False,
                                            isCeltsAdmin = False,
                                            isCeltsStudentStaff = True)
    
        testAdminCreationUser2 = User.create(username = "testAdminCreationUser2",
                                            bnumber = "B92236789",
                                            email = "testAdminCreationUser2@berea.edu",
                                            phoneNumber = "(859)876-5309",
                                            firstName = "Test",
                                            lastName = "AdminCreation",
                                            isStudent = False,
                                            isFaculty = True,
                                            isStaff = False,
                                            isCeltsAdmin = False,
                                            isCeltsStudentStaff = True)
        
        assert testAdminCreationUser1.isCeltsAdmin == False
        assert testAdminCreationUser1.isCeltsStudentStaff == True
    
        assert testAdminCreationUser2.isCeltsAdmin == False
        assert testAdminCreationUser2.isFaculty == True

        # Testing step 2
        with app.app_context():
            g.current_user = "ramsayb2"

            addCeltsAdmin(testAdminCreationUser1)
            testAdminCreationUser1 = User.get(User.username == testAdminCreationUser1)
            assert testAdminCreationUser1.isCeltsAdmin == True

            addCeltsAdmin(testAdminCreationUser2)
            testAdminCreationUser2 = User.get(User.username == testAdminCreationUser2)
            assert testAdminCreationUser2.isCeltsAdmin == True

        # Testing step 3
        with app.app_context():
            g.current_user = "ramsayb2"

            with pytest.raises(Exception):
                addCeltsAdmin(testAdminCreationUser1)

            with pytest.raises(Exception):
                addCeltsAdmin(testAdminCreationUser2)

        # Testing step 4
        with app.app_context():
            g.current_user = "ramsayb2"
            
            removeCeltsAdmin(testAdminCreationUser1)
            testAdminCreationUser1 = User.get(User.username == testAdminCreationUser1)
            assert testAdminCreationUser1.isCeltsAdmin == False

            removeCeltsAdmin(testAdminCreationUser2)
            testAdminCreationUser2 = User.get(User.username == testAdminCreationUser2)
            assert testAdminCreationUser2.isCeltsAdmin == False

        # Testing step 5
        testInvalidAdminCreationUser = User.create(username = "testInvalidAdminCreationUser",
                                            bnumber = "B98732289",
                                            email = "testInvalidAdminCreationUser@berea.edu",
                                            phoneNumber = "(859)876-5309",
                                            firstName = "Test",
                                            lastName = "InvalidAdminCreation",
                                            isStudent = True,
                                            isFaculty = False,
                                            isStaff = False,
                                            isCeltsAdmin = False,
                                            isCeltsStudentStaff = False)
        
        # Testing step 6
        with app.app_context():
            g.current_user = "ramsayb2"
            with pytest.raises(Exception):
                addCeltsAdmin(testInvalidAdminCreationUser)

        # Testing step 7
        with app.app_context():
            g.current_user = "ramsayb2"
            with pytest.raises(Exception):
                addCeltsAdmin("blahbah")
            with pytest.raises(Exception):
                addCeltsAdmin("ksgvoidsid;")

        # Testing step 8
        transaction.rollback()

@pytest.mark.integration
def test_modifyCeltsStudentStaff():
    """
    A function that tests the addCeltsStudentStaff and removeCeltsStudentStaff functions. 
    
    Testing steps:

    1. Creates a new user that is just a student.
    2. Verify that the new user can be added as a student staff.
    3. Make sure an error gets thrown when we try to add the user as a student staff again.
    4. Make the new student staff a program manager for a couple of programs.
    5. Verify that the user we just added can be removed successfully.
    6. Now that the user is no longer a student staff, check they are not the program manager for any programs either.
    7. Create a new user that is a faculty.
    8. Make sure an error gets thrown when we add a user that is not a student.
    9. Make sure an error gets thrown when we try to add users that don't exist.
    10. Rollback changes.
    """
    with mainDB.atomic() as transaction:

        # Testing step 1
        testStudentStaffCreationUser = User.create(username = "testStudentStaffCreationUser",
                                            bnumber = "B00775209",
                                            email = "testStudentStaffCreationUser@berea.edu",
                                            phoneNumber = "(859)876-5309",
                                            firstName = "Test",
                                            lastName = "StudentStaffCreation",
                                            isStudent = True,
                                            isFaculty = False,
                                            isStaff = False,
                                            isCeltsAdmin = False,
                                            isCeltsStudentStaff = False)     
           
        assert testStudentStaffCreationUser.isCeltsStudentStaff == False
        assert testStudentStaffCreationUser.isStudent == True

        # Testing step 2
        with app.app_context():
            g.current_user = "ramsayb2"

            addCeltsStudentStaff(testStudentStaffCreationUser)
            testStudentStaffCreationUser = User.get(User.username == testStudentStaffCreationUser)
            assert testStudentStaffCreationUser.isCeltsStudentStaff == True

        # Testing step 3
        with pytest.raises(Exception):
            addCeltsStudentStaff(testStudentStaffCreationUser)

        # Testing step 4
        with app.app_context():
            g.current_user = "ramsayb2"
            ProgramManager.create(user=testStudentStaffCreationUser, program=1)
            ProgramManager.create(user=testStudentStaffCreationUser, program=2)
            userManagedPrograms = list(ProgramManager.select(Program).join(Program).where(ProgramManager.user == testStudentStaffCreationUser))
            assert len(userManagedPrograms) == 2

        # Testing step 5
        with app.app_context():
            g.current_user = "ramsayb2"
            removeCeltsStudentStaff(testStudentStaffCreationUser)
            testStudentStaffCreationUser = User.get(User.username == testStudentStaffCreationUser)
            assert testStudentStaffCreationUser.isCeltsStudentStaff == False
        
        # Testing step 6
        userManagedPrograms = list(ProgramManager.select(Program).join(Program).where(ProgramManager.user == testStudentStaffCreationUser))
        assert len(userManagedPrograms) == 0

        # Testing step 7
        testInvalidStudentStaffCreationUser = User.create(username = "testInvalidStudentStaffCreationUser",
                                            bnumber = "B00775208",
                                            email = "testInvalidStudentStaffCreationUser@berea.edu",
                                            phoneNumber = "(859)876-5309",
                                            firstName = "Test",
                                            lastName = "InvalidStudentStaffCreation",
                                            isStudent = False,
                                            isFaculty = True,
                                            isStaff = False,
                                            isCeltsAdmin = False,
                                            isCeltsStudentStaff = False) 

        # Testing step 8
        with app.app_context():
            g.current_user = "ramsayb2"
            with pytest.raises(Exception):
                addCeltsStudentStaff(testInvalidStudentStaffCreationUser)

        # Testing step 9
        with app.app_context():
            g.current_user = "ramsayb2"
            with pytest.raises(Exception):
                addCeltsStudentStaff("asdf")
            with pytest.raises(Exception):
                removeCeltsStudentStaff("1234")

        # Testing step 10
        transaction.rollback()


@pytest.mark.integration
def test_modifyCeltsStudentAdmin():
    """
    A function that tests the addCeltsAdmin and removeCeltsAdmin functions. 
    
    Testing steps:

    1. Create a new user that is just a student.
    2. Verify that the new user can be added as a student admin.
    3. Make sure an error gets thrown when we try to add the user again.
    4. Verify that the user we just added can be removed successfully.
    5. Create a new user that is a faculty, not a student.
    6. Make sure an error gets thrown when we add a user that is not a student.
    7. Make sure an error gets thrown when we try to add users that don't exist.
    8. Rollback changes.
    """
    with mainDB.atomic() as transaction:
        # Testing step 1
        testStudentAdminCreationUser: User = User.create(username = "testStudentAdminCreationUser",
                                            bnumber = "B00775219",
                                            email = "testStudentAdminCreationUser@berea.edu",
                                            phoneNumber = "(859)876-5309",
                                            firstName = "Test",
                                            lastName = "StudentAdminCreation",
                                            isStudent = True,
                                            isFaculty = False,
                                            isStaff = False,
                                            isCeltsAdmin = False,
                                            isCeltsStudentStaff = False)   
               
        assert testStudentAdminCreationUser.isCeltsStudentAdmin == False
        assert testStudentAdminCreationUser.isStudent == True

        # Testing step 2
        with app.app_context():
            g.current_user = "qasema"
            addCeltsStudentAdmin(testStudentAdminCreationUser)
            testStudentAdminCreationUser = User.get(User.username == testStudentAdminCreationUser)
            assert testStudentAdminCreationUser.isCeltsStudentAdmin == True

        # Testing step 3
        with pytest.raises(Exception):
            addCeltsStudentStaff(testStudentAdminCreationUser)

        # Testing step 4
        with app.app_context():
            g.current_user = "qasema"
            removeCeltsStudentAdmin(testStudentAdminCreationUser)
            testStudentAdminCreationUser = User.get_by_id(testStudentAdminCreationUser)
            assert testStudentAdminCreationUser.isCeltsStudentAdmin == False

        # Testing Step 6
        testNonStudent = User.create(username = "testNonStudent",
                                  bnumber = "B00775209",
                                  email = "testNonStudent@berea.edu",
                                  phoneNumber = "(859)876-5309",
                                  firstName = "Test",
                                  lastName = "NonStudent",
                                  isStudent = False,
                                  isFaculty = True,
                                  isStaff = False,
                                  isCeltsAdmin = False,
                                  isCeltsStudentStaff = False)
        
        # Testing step 6
        with pytest.raises(Exception):
            g.current_user = "qasema"
            addCeltsStudentAdmin(testNonStudent)
        
        # Testing step 7
        with app.app_context():
            g.current_user = "ramsayb2"
            with pytest.raises(Exception):
                addCeltsStudentAdmin("TH1SUSERDEFDONTEX1ST")
            with pytest.raises(Exception):
                addCeltsStudentAdmin("!TH1SUS,,,...ERPRDONTEX1STEither")

        # Testing step 8
        transaction.rollback()

@pytest.mark.integration
def test_changeProgramInfo():
    with mainDB.atomic() as transaction:

        programId = 3
        eventName = "Test Event Name"
        contactName = "New Test Name"
        contactEmail = 'newtest@email'
        location = "Danforth Tech"
        currentProgramInfo = Program.get_by_id(programId)

        assert currentProgramInfo.programName == "Adopt-a-Grandparent"
        assert currentProgramInfo.contactName == ""
        assert currentProgramInfo.contactEmail == ""
        assert currentProgramInfo.defaultLocation == ""

        with app.test_request_context():
            g.current_user = "ramsayb2"
            changeProgramInfo(eventName, contactEmail, contactName, location, programId)

        currentProgramInfo = Program.select().where(Program.id==programId).get()

        assert currentProgramInfo.programName == eventName
        assert currentProgramInfo.contactName == contactName
        assert currentProgramInfo.contactEmail == contactEmail
        assert currentProgramInfo.defaultLocation == location

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

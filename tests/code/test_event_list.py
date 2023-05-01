import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.event import Event
from app.models.bonnerCohort import BonnerCohort
from app.models.term import Term
from app.models.user import User
from app.models.eventViews import EventView
from app.logic.events import getStudentLedEvents,  getTrainingEvents, getBonnerEvents, getOtherEvents, addEventView

@pytest.mark.integration
@pytest.fixture
# pytest fixture: used to setup the test data that can be resused in all of the
# tests.
def training_events():
    testEvent = Event.create(name = "Test Student Lead",
                             term = 2,
                             description = "event for testing",
                             timeStart = "18:00:00",
                             timeEnd = "21:00:00",
                             location = "basement",
                             isTraining = True,
                             startDate = "2021-12-12",
                             endDate = "2021-12-13")

    testProgramEvent = ProgramEvent.create(program = 2 , event = testEvent)

    yield testProgramEvent
    testEvent.delete_instance(testProgramEvent)

@pytest.mark.integration
@pytest.fixture
def special_bonner():
    bonnerEvent = Event.create(name = "Test For Bonner",
                               term = 2,
                               description = "Special event test for Bonner",
                               timeStart = "19:00:00",
                               timeEnd = "22:00:00",
                               location = "moon",
                               startDate = "2021-12-12",
                               endDate = "2021-12-13")

    specialForBonner = ProgramEvent.create(program = 5, event = bonnerEvent)

    yield specialForBonner
    bonnerEvent.delete_instance(specialForBonner)

@pytest.mark.integration
@pytest.fixture
def special_otherEvents():
        nonProgramEvent = Event.create(name = "Test for nonProgram",
                                       term = 4,
                                       description = "Special event test for nonProgram",
                                       timeStart = "19:00:00",
                                       timeEnd = "22:00:00",
                                       location = "moon",
                                       isTraining = False,
                                       startDate = "2021-12-12",
                                       endDate = "2021-12-13")

        yield nonProgramEvent
        nonProgramEvent.delete_instance()

@pytest.mark.integration
def test_studentled_events(training_events):
    studentLed = training_events
    allStudentLedProgram = {studentLed.program: [studentLed.event]}

    assert allStudentLedProgram == getStudentLedEvents(2)

@pytest.mark.integration
def test_training_events(training_events):
    with mainDB.atomic() as transaction:
        testTerm = Term.create( description = "Test Term",
                                year = 1919,
                                academicYear = "1919-1920",
                                isSummer = False,
                                isCurrentTerm = False)
       
        testBonnerProgram = Program.create(programName = "Test Bonner",
                                           partner = None,
                                           isStudentLed = False,
                                           isBonnerScholars = True,
                                           contactName = "Jesus Christ",
                                           contactEmail = "christj@test.com")
        
        testNotBonnerProgram = Program.create(programName = "Test Not Bonner",
                                              partner = None,
                                              isStudentLed = False,
                                              isBonnerScholars = False,
                                              contactName = "Jesus Christ",
                                              contactEmail = "christj@test.com")
       
        testBonnerTraining = Event.create(name = "Bonner Test Training",
                                          term = testTerm,
                                          description = "Bonner Test Training",
                                          timeStart = "18:00:00",
                                          timeEnd = "21:00:00",
                                          location = "basement",
                                          isTraining = True,
                                          startDate = "1919-12-13",
                                          endDate = "1919-12-14")
       
        testNotBonnerTraining = Event.create(name = "Bonner Test Training",
                                             term = testTerm,
                                             description = "Not Bonner",
                                             timeStart = "18:00:00",
                                             timeEnd = "21:00:00",
                                             location = "basement",
                                             isTraining = True,
                                             startDate = "1919-12-12",
                                             endDate = "1919-12-13")
        
        ProgramEvent.create(program = testBonnerProgram.id, event = testBonnerTraining)
        ProgramEvent.create(program = testNotBonnerProgram.id, event = testNotBonnerTraining)
        ProgramEvent.create(program = 1, event = testNotBonnerTraining)

        userFaculty = User.create(username = "TestNotBonner",
                                  bnumber = "B000000000",
                                  email = "test@test.com",
                                  phoneNumber = "000-000-0000",
                                  firstName = "TestFirst",
                                  lastName = "TestLast",
                                  isStudent = False,
                                  isFaculty = True,
                                  isStaff = False,
                                  isCeltsAdmin = False,
                                  isCeltsStudentStaff = False)
       
        userStaff = User.create(username = "TestisStaff",
                                bnumber = "B00000000002",
                                email = "test@test.com",
                                phoneNumber = "000-000-0000",
                                firstName = "TestFirst",
                                lastName = "TestLast",
                                isStudent = False,
                                isFaculty = False,
                                isStaff = True,
                                isCeltsAdmin = False,
                                isCeltsStudentStaff = False)
        
        userCeltsAdmin = User.create(username = "TestisCeltsAdmin",
                                     bnumber = "B00000000003",
                                     email = "test@test.com",
                                     phoneNumber = "000-000-0000",
                                     firstName = "TestFirst",
                                     lastName = "TestLast",
                                     isStudent = False,
                                     isFaculty = False,
                                     isStaff = False,
                                     isCeltsAdmin = True,
                                     isCeltsStudentStaff = False)
      
        userBonnerScholar = User.create(username = "TestBonnerScholar",
                                        bnumber = "B0000000000",
                                        email = "test@test.com",
                                        phoneNumber = "000-000-0000",
                                        firstName = "TestFirst",
                                        lastName = "TestLast",
                                        isStudent = True,
                                        isFaculty = False,
                                        isStaff = False,
                                        isCeltsAdmin = False,
                                        isCeltsStudentStaff = False)
       
        BonnerCohort.create(user=userBonnerScholar, year=2020)

        userNotBonnerScholar = User.create(username = "TestNotBonnerScholar",
                                           bnumber = "B00000000001",
                                           email = "test@test.com",
                                           phoneNumber = "000-000-0000",
                                           firstName = "TestFirst",
                                           lastName = "TestLast",
                                           isStudent = True,
                                           isFaculty = False,
                                           isStaff = False,
                                           isCeltsAdmin = False,
                                           isCeltsStudentStaff = False)

        notBonnerList = [testNotBonnerTraining]
        bonnerList = [testNotBonnerTraining, testBonnerTraining]

        assert notBonnerList == getTrainingEvents(testTerm, userFaculty)
        assert notBonnerList == getTrainingEvents(testTerm, userNotBonnerScholar)
        assert notBonnerList == getTrainingEvents(testTerm, userStaff)
        assert bonnerList == getTrainingEvents(testTerm, userCeltsAdmin)
        assert bonnerList == getTrainingEvents(testTerm, userBonnerScholar)

        transaction.rollback()

@pytest.mark.integration
def test_bonner_events(special_bonner):
    bonner = special_bonner
    allBonnerProgram = [bonner.event]

    assert allBonnerProgram == getBonnerEvents(2)

@pytest.mark.integration
def test_getOtherEvents(special_otherEvents):
    otherEvent = special_otherEvents
    otherEvents = [Event.get_by_id(11), Event.get_by_id(7), otherEvent]
    
    assert otherEvents == getOtherEvents(4)

@pytest.mark.integration
def test_eventViewCount():
    with mainDB.atomic() as transaction:
        testEvent = Event.create(name = "Test Student view",
                                 term = 2,
                                 description = "event for testing",
                                 timeStart = "18:00:00",
                                 timeEnd = "21:00:00",
                                 location = "basement",
                                 isTraining = True,
                                 startDate = "2021-12-12",
                                 endDate = "2021-12-13")
        viewer = User.create(username = "eventViewer",
                             bnumber = "B000000000",
                             email = "test@test.com",
                             phoneNumber = "000-000-0000",
                             firstName = "TestFirst",
                             lastName = "TestLast",
                             isStudent = False,
                             isFaculty = True,
                             isStaff = False,
                             isCeltsAdmin = False,
                             isCeltsStudentStaff = False)
        admineView = User.create(username = "admineViewer",
                                 bnumber = "B000000001",
                                 email = "test@test.com",
                                 phoneNumber = "000-000-0000",
                                 firstName = "TestFirst",
                                 lastName = "TestLast",
                                 isStudent = False,
                                 isFaculty = True,
                                 isStaff = False,
                                 isCeltsAdmin = True,
                                 isCeltsStudentStaff = False)        
        
        addEventView(viewer,testEvent)
        assert EventView.select().where(EventView.user == viewer, EventView.event == testEvent).exists()
        
        addEventView(viewer,testEvent) # to check that no more than one record for the same user and the same event
        assert( EventView.select().where(EventView.user == viewer, EventView.event == testEvent).count() ==1 ) 
        
        addEventView(admineView,testEvent) # to check that admin view is not recorded 
        assert not EventView.select().where(EventView.user == admineView, EventView.event == testEvent).exists()
        transaction.rollback() 

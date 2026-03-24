import pytest
from peewee import DoesNotExist
from datetime import datetime, date

from app.models import mainDB
from app.models.program import Program
from app.models.event import Event
from app.models.bonnerCohort import BonnerCohort
from app.models.term import Term
from app.models.user import User
from app.models.eventViews import EventView
from app.logic.events import getVolunteerOpportunities, getEngagementEvents, getTrainingEvents, getBonnerEvents, getCeltsLabor, addEventView, getUpcomingVolunteerOpportunitiesCount

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
                             program = 2)

    yield testEvent
    testEvent.delete_instance(testEvent)

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
                               program = 5)


    yield bonnerEvent
    bonnerEvent.delete_instance(bonnerEvent)

@pytest.mark.integration
@pytest.fixture
def special_celtsLabor():
        nonProgramEvent = Event.create(name = "Test for nonProgram",
                                       term = 4,
                                       description = "Special event test for nonProgram",
                                       timeStart = "19:00:00",
                                       timeEnd = "22:00:00",
                                       location = "moon",
                                       isTraining = False,
                                       startDate = "2021-12-12",
                                       program = 9)

        yield nonProgramEvent
        nonProgramEvent.delete_instance()

@pytest.mark.integration
def test_getVolunteerOpportunities(training_events):

    training_events.term = 2
    training_events.isService = True
    training_events.deletionDate = None
    training_events.save()
    training_events.program.save()

    expected = {training_events.program: [training_events]}
    actual = getVolunteerOpportunities(2)
    assert expected == actual

@pytest.mark.integration
def test_getUpcomingVolunteerOpportunitiesCount():
    with mainDB.atomic() as transaction: 
        testDate = datetime.strptime("08/01/2021 05:00","%m/%d/%Y %H:%M")
        currentTestTerm = Term.get_by_id(5)

        # In case any events are put in term 5 in testData, put them into the past.
        Event.update(startDate = date(2021,7,1)).where(Event.term_id == 5).execute()

        # Volunteer Opportunitiesevent in the future
        futureAgpEvent = Event.create(name = "Test future AGP event",
                                      term = currentTestTerm,
                                      description = "Test future volunteer opportunities(AGP) event.",
                                      timeStart = "05:00:00",
                                      timeEnd = "06:00:00",
                                      location = "The Moon",
                                      isTraining = False,
                                      isService = True,
                                      startDate = "2021-08-02",
                                      program = 3)
         
        # Volunteer Opportunitiesevent to be canceled 
        cancelVolunteerOpportunities = Event.create(name = "Test AGP event to cancel",
                                        term = currentTestTerm,
                                        description = "Test volunteer opportunities(AGP) event that will be canceled.",
                                        timeStart = "05:00:00",
                                        timeEnd = "06:00:00",
                                        location = "The Sun",
                                        isTraining = False,
                                        isService = True,
                                        startDate = "2021-08-02",
                                        program = 3)
        
        # Volunteer Opportunitiesevent that start in the future but will be moved to the past
        pastVolunteerOpportunities = Event.create(name = "Test past AGP event",
                                        term = currentTestTerm,
                                        description = "Test volunteer opportunities(AGP) event that will be moved to the past.",
                                        timeStart = "05:00:00",
                                        timeEnd = "06:00:00",
                                        location = "Mars",
                                        isTraining = False,
                                        isService = True,
                                        startDate = "2021-08-02",
                                        program = 3)
        
        # verify that there are three upcoming events for AGP (program id 3)
        upcomingVolunteerOpportunities = getUpcomingVolunteerOpportunitiesCount(currentTestTerm, testDate)
        assert upcomingVolunteerOpportunities == {3:3}

        # Cancel cancelVolunteerOpportunities and verify there are only two upcoming events for AGP
        Event.update(isCanceled = True).where(Event.id == cancelVolunteerOpportunities.id).execute()
        upcomingVolunteerOpportunities = getUpcomingVolunteerOpportunitiesCount(currentTestTerm, testDate)
        assert upcomingVolunteerOpportunities == {3:2}

        # Move pastVolunteerOpportunities start date to the same day as testDate and set timeEnd to the time on testDate
        (Event.update(timeStart = datetime.strptime("03:00", "%H:%M").time(), 
                      timeEnd = datetime.strptime("04:00", "%H:%M").time(), 
                      startDate = date(2021,8,1))
              .where(Event.id == pastVolunteerOpportunities.id)).execute()
        
        upcomingVolunteerOpportunities = getUpcomingVolunteerOpportunitiesCount(currentTestTerm, testDate)
        assert upcomingVolunteerOpportunities == {3:1}

        # Create another event in the future for a different program (Buddies)
        futureBuddiesEvent = Event.create(name = "Test future AGP event",
                                          term = currentTestTerm,
                                          description = "Test future volunteer opportunities(AGP) event.",
                                          timeStart = "05:00:00",
                                          timeEnd = "06:00:00",
                                          location = "The Moon",
                                          isTraining = False,
                                          isService = True,
                                          startDate = "2021-08-02",
                                          program = 2)
        
        upcomingVolunteerOpportunities = getUpcomingVolunteerOpportunitiesCount(currentTestTerm, testDate)
        assert upcomingVolunteerOpportunities == {2:1, 3:1}

        transaction.rollback()

@pytest.mark.integration
def test_getTrainingEvents(training_events):
    with mainDB.atomic() as transaction:
        testTerm = Term.create( description = "Test Term",
                                year = 1919,
                                academicYear = "1919-1920",
                                isSummer = False,
                                isCurrentTerm = False)
       
        testBonnerProgram = Program.create(programName = "Test Bonner",
                                           partner = None,
                                           isBonnerScholars = True,
                                           contactName = "Jesus Christ",
                                           contactEmail = "christj@test.com",)
        
        testNotBonnerProgram = Program.create(programName = "Test Not Bonner",
                                              partner = None,
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
                                          program = testBonnerProgram.id)
       
        testNotBonnerTraining = Event.create(name = "Bonner Test Training",
                                             term = testTerm,
                                             description = "Not Bonner",
                                             timeStart = "18:00:00",
                                             timeEnd = "21:00:00",
                                             location = "basement",
                                             isTraining = True,
                                             startDate = "1919-12-12",
                                             program = testNotBonnerProgram.id)

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
def test_getBonnerEvents(special_bonner):
    bonner = special_bonner
    allBonnerProgram = [bonner]
    assert allBonnerProgram == getBonnerEvents(2)

@pytest.mark.integration
def test_getEngagementEvents():
    with mainDB.atomic() as transaction:
        testTerm = Term.create( description = "Test Term",
                                year = 1919,
                                academicYear = "1919-1920",
                                isSummer = False,
                                isCurrentTerm = False)
        
        engagementEvent = Event.create(name = "Bonner Test Training",
                                             term = testTerm,
                                             description = "Not Bonner",
                                             timeStart = "18:00:00",
                                             timeEnd = "21:00:00",
                                             location = "basement",
                                             isEngagement = True,
                                             startDate = "1919-12-12",
                                             program = 1)
        
        returnedEvent = getEngagementEvents(testTerm)
        returnedNonEngEvent = getEngagementEvents(2)
        assert len(returnedEvent) == 1
        assert len(returnedNonEngEvent) == 0
        assert returnedEvent == [engagementEvent]

        transaction.rollback()

@pytest.mark.integration
def test_getCeltsLabor(special_celtsLabor):
    expected = list(
    Event.select()
    .where(Event.term == 4, Event.deletionDate == None, Event.isLaborOnly == True)
    .order_by(Event.startDate, Event.timeStart, Event.id))
    assert expected == getCeltsLabor(4)

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
                                 program = 9)
        
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
       
        adminView = User.create(username = "adminViewer",
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
        
        addEventView(adminView,testEvent) # to check that admin view is not recorded 
        assert not EventView.select().where(EventView.user == adminView, EventView.event == testEvent).exists()
        transaction.rollback() 

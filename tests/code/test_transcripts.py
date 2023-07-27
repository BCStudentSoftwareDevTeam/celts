import pytest
from peewee import DoesNotExist
from flask import g
from app import app

from app.logic.transcript import *
from app.models.user import User
from app.models.courseParticipant import CourseParticipant
from app.models.event import Event
from app.logic.events import deleteEvent

@pytest.fixture(autouse=True)
def setup():
    testUser = User.create(
                        username = "namet",
                        bnumber = "B001234567",
                        email = "namet@berea.edu",
                        phoneNumber = "555-123-1234",
                        firstName = "Test",
                        lastName  = "Name",
                        isStudent = 1,
                        isFaculty = 0,
                        isCeltsAdmin = 0,
                        isCeltsStudentStaff = 0,
                        )

    newTrainingEvent = Event.create(name = "Test Training Event",
                              term = 1,
                              description= "Event for testing",
                              timeStart = "18:00:00",
                              timeEnd = "21:00:00",
                              location = "The testing lab",
                              isRsvpRequired = 0,
                              isPrerequisiteForProgram = 0,
                              isTraining = 1,
                              isService = 0,
                              startDate =  "2021-12-12",
                              endDate =  "2021-12-13",
                              recurringId = None,
                              program_id=2)

    EventParticipant.create(user = testUser,
                            event = newTrainingEvent,
                            attended = True,
                            hoursEarned = 2)


    newBonnerEvent = Event.create(name = "Test Bonner Event",
                              term = 1,
                              description= "Event for testing",
                              timeStart = "18:00:00",
                              timeEnd = "21:00:00",
                              location = "The testing lab",
                              isRsvpRequired = 0,
                              isPrerequisiteForProgram = 0,
                              isTraining = 0,
                              isService = 0,
                              startDate =  "2021-12-12",
                              endDate =  "2021-12-13",
                              recurringId = None,
                              program_id= 5)
    
    EventParticipant.create(user = testUser,
                            event = newBonnerEvent,
                            attended = True,
                            hoursEarned = 2)


    adminName = "ramsayb2"

    newCourse = Course.create(courseName = "Test Course",
                                term = 1,
                                status = 1,
                                courseCredit = "45",
                                createdBy = "ramsayb2",
                                isAllSectionsServiceLearning = 0,
                                isPermanentlyDesignated = 0,
                                sectionBQuestion1 = "",
                                sectionBQuestion2 = "",
                                sectionBQuestion3 = "",
                                sectionBQuestion4 = "",
                                sectionBQuestion5 = "",
                                sectionBQuestion6 = "")

    CourseInstructor.create(course = newCourse, user = adminName)
    CourseParticipant.create(course = newCourse, user = testUser, hoursEarned = 3.0)

    newProgramEvent = Event.create(name = "Test Program Event",
                              term = 1,
                              description= "Event for testing",
                              timeStart = "18:00:00",
                              timeEnd = "21:00:00",
                              location = "The testing lab",
                              isRsvpRequired = 0,
                              isPrerequisiteForProgram = 0,
                              isTraining = 0,
                              isService = 0,
                              startDate =  "2021-12-12",
                              endDate =  "2021-12-13",
                              recurringId = None,
                              program_id= 1)

    EventParticipant.create(user = testUser,
                            event = newProgramEvent,
                            attended = True,
                            hoursEarned = 2)


    newNonProgramEvent = Event.create(name = "Test Non-Program Event",
                              term = 3,
                              description= "Event for testing",
                              timeStart = "18:00:00",
                              timeEnd = "21:00:00",
                              location = "The testing lab",
                              isRsvpRequired = 0,
                              isPrerequisiteForProgram = 0,
                              isTraining = 0,
                              isService = 0,
                              startDate =  "2021-12-12",
                              endDate =  "2021-12-13",
                              recurringId = None,
                              program_id = 9)
    EventParticipant.create(user = testUser,
                            event = newNonProgramEvent,
                            attended = True,
                            hoursEarned = 2)

@pytest.fixture(autouse=True)
def teardown():
    yield

    testingTrainingEvent = Event.get(Event.name == "Test Training Event")
    testingTrainingEvent.delete_instance(recursive=True, delete_nullable=True)

    # delete bonner
    testingBonnerEvent = Event.get(Event.name == "Test Bonner Event")
    testingBonnerEvent.delete_instance(recursive=True, delete_nullable=True)

    # delete courses
    testingCourse = Course.get(Course.courseName == "Test Course")
    testingCourse.delete_instance(recursive=True, delete_nullable=True)

    # delete program
    testingProgramEvent = Event.get(Event.name == "Test program Event")
    testingProgramEvent.delete_instance(recursive=True, delete_nullable=True)

    # delete program
    testingProgramEvent = Event.get(Event.name == "Test Non-Program Event")
    testingProgramEvent.delete_instance(recursive=True, delete_nullable=True)

    # delete user
    user = User.get(User.username == "namet")
    user.delete_instance(recursive=True, delete_nullable=True)

@pytest.mark.integration
def testingSLCourses():

    username = "namet"
    adminName = "ramsayb2"

    testingSLCExist= getSlCourseTranscript(username)
    testingSLCNotExist = getSlCourseTranscript(adminName)

    checkingNewCourse = Course.get(Course.courseName == "Test Course")

    assert not testingSLCNotExist.exists()
    assert testingSLCExist.exists()
    assert checkingNewCourse in testingSLCExist


@pytest.mark.integration
def testingProgram():

    username = "namet"
    adminName = "ramsayb2"
    programDict = getProgramTranscript(username)
    emptyProgramDict = getProgramTranscript(adminName)
    # check that bonners events are caught
    checkingProgram = Program.get_by_id(5)

    assert not emptyProgramDict
    assert programDict
    assert checkingProgram in [t for t in programDict]

@pytest.mark.integration
def testingOtherEventsTranscript():

    username = "namet"
    adminName = "ramsayb2"
    otherDict = getOtherEventsTranscript(username)
    emptyOtherDict = getOtherEventsTranscript(adminName)

    checkingOtherEvent = Event.get(Event.name == "Test Non-Program Event")
    participatedEvent = EventParticipant.get(EventParticipant.user == username, EventParticipant.event == checkingOtherEvent)
    termInfo = [checkingOtherEvent.term.description, participatedEvent.hoursEarned]


    assert not emptyOtherDict
    assert otherDict
    assert termInfo in [t for t in otherDict]

@pytest.mark.integration
def testingGetAllEventTranscript():

    username = "namet"
    adminName = "ramsayb2"
    allEventDict = getAllEventTranscript(username)
    emptyAllEventDict = getAllEventTranscript(adminName)
    # check that bonners events are caught
    checkingProgram = Program.get_by_id(5)

    checkingOtherEvent = Event.get(Event.name == "Test Non-Program Event")
    participatedEvent = EventParticipant.get(EventParticipant.user == username, EventParticipant.event == checkingOtherEvent)
    termInfo = [checkingOtherEvent.term.description, participatedEvent.hoursEarned]

    # ensures the results of both child function appear in the same dictionary
    assert not emptyAllEventDict
    assert allEventDict
    print(allEventDict)
    assert checkingProgram in [t for t in allEventDict] and termInfo in allEventDict["CELTS Sponsored Events"]


@pytest.mark.integration
def testingTotalHours():

    totalHours = getTotalHours("namet")
    assert totalHours["totalCourseHours"] == 3
    assert totalHours["totalEventHours"] == 8
    assert totalHours["totalHours"] == 11

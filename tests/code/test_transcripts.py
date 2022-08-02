import pytest
from peewee import DoesNotExist
from flask import g
from app import app

from app.logic.transcript import *
from app.models.user import User
from app.models.courseParticipant import CourseParticipant
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.models.eventFacilitator import EventFacilitator
from app.logic.events import deleteEvent

@pytest.mark.integration
def setup_module():
    with app.app_context():
        g.current_user = User.get_by_id("ramsayb2")
    user = User.create(
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
                              recurringId = None)

    programEvent = ProgramEvent.create(program=2, event=newTrainingEvent)

    facilitatorEntry = EventFacilitator.create(user = 'ramsayb2',event = newTrainingEvent)

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
                              recurringId = None)

    programEvent = ProgramEvent.create(program=5, event=newBonnerEvent)

    facilitatorEntry = EventFacilitator.create(user = 'ramsayb2',event = newBonnerEvent)

    username = "namet"
    adminName = "ramsayb2"

    newCourse = Course.create(courseName = "Test Course",
                                term = 1,
                                status = 1,
                                courseCredit = "45",
                                createdBy = "ramsayb2",
                                isAllSectionsServiceLearning = 0,
                                isPermanentlyDesignated = 0,
                                sectionBQuestion1 = "CharField()",
                                sectionBQuestion2 = "CharField()",
                                sectionBQuestion3 = "CharField()",
                                sectionBQuestion4 = "CharField()",
                                sectionBQuestion5 = "CharField()",
                                sectionBQuestion6 = "CharField()")

    testingCourse = Course.get(Course.courseName == "Test Course")
    instructor = CourseInstructor.create(course = testingCourse.id, user = adminName)
    courseParticipant = CourseParticipant.create(course = testingCourse.id,
                                                    user = username,
                                                    hoursEarned = 3.0)

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
                              recurringId = None)

    programEvent = ProgramEvent.create(program=1, event=newProgramEvent)

    testingTrainingEvent = Event.get(Event.name == "Test Training Event")
    trainingpart = EventParticipant.create(user = "namet",
                                            event = testingTrainingEvent.id,
                                            attended = True,
                                            hoursEarned = 2)

    testingBonnerEvent = Event.get(Event.name == "Test Bonner Event")
    trainingpart = EventParticipant.create(user = "namet",
                                            event = testingBonnerEvent.id,
                                            attended = True,
                                            hoursEarned = 2)

    testingProgramEvent = Event.get(Event.name == "Test Program Event")
    trainingpart = EventParticipant.create(user = "namet",
                                            event = testingProgramEvent.id,
                                            attended = True,
                                            hoursEarned = 2)

@pytest.mark.integration
def testingSLCourses():

    username = "namet"
    adminName = "ramsayb2"

    testingSLCExist= getSlCourseTranscript(username)
    testingSLCNotExist = getSlCourseTranscript(adminName)

    checkingNewCourse = Course.get(courseName = "Test Course")

    assert not testingSLCNotExist.exists()
    assert testingSLCExist.exists()
    assert checkingNewCourse in testingSLCExist


@pytest.mark.integration
def testingProgram():

    username = "namet"
    adminName = "ramsayb2"
    testingProgramExist = getProgramTranscript(username)
    testingProgramNotExist = getProgramTranscript(adminName)
    # check that bonners events are caught
    checkingProgram = Program.get_by_id(5)

    assert not testingProgramNotExist
    assert testingProgramExist
    assert checkingProgram in [t for t in testingProgramExist]


@pytest.mark.integration
def testingTotalHours():

    totalHours = getTotalHours("namet")
    assert totalHours["totalCourseHours"] == 3
    assert totalHours["totalEventHours"] == 6
    assert totalHours["totalHours"] == 9

@pytest.mark.integration
def teardown_module():
    with app.app_context():
        g.current_user = User.get_by_id("ramsayb2")
        testingTrainingEvent = Event.get(Event.name == "Test Training Event")
        deleteEvent(testingTrainingEvent)
        assert Event.get_or_none(Event.id == testingTrainingEvent) is None
        # delete bonner
        testingBonnerEvent = Event.get(Event.name == "Test Bonner Event")
        deleteEvent(testingBonnerEvent)
        assert Event.get_or_none(Event.id == testingBonnerEvent) is None
        # delete courses
        testingCourse = Course.get(Course.courseName == "Test Course")
        testingCourse.delete_instance(recursive = True, delete_nullable = True)
        assert Course.get_or_none(Course.id == testingCourse.id) is None
        # delete program
        testingProgramEvent = Event.get(Event.name == "Test program Event")
        deleteEvent(testingProgramEvent)
        assert Event.get_or_none(Event.id == testingProgramEvent) is None
        # delete user
        user = User.get(User.username == "namet")
        user.delete_instance(recursive = True, delete_nullable = True)
        assert User.get_or_none(User.username == "namet") is None

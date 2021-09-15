import pytest
from peewee import DoesNotExist

from app.logic.transcript import *
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator
from app.logic.volunteers import addVolunteerToEvent
from app.logic.events import deleteEvent


@pytest.mark.integration
def testingTrainings():

    newEvent = Event.create(eventName = "Test Event",
                              term = 1,
                              description= "Event for testing",
                              timeStart = "18:00:00",
                              timeEnd = "21:00:00",
                              location = "The testing lab",
                              isRecurring = 0,
                              isRsvpRequired = 0,
                              isPrerequisiteForProgram = 0,
                              isTraining = 1,
                              isService = 0,
                              startDate =  2021-12-12,
                              endDate =  2021-12-13)

    programEvent = ProgramEvent.create(program=2, event=newEvent)

    facilitatorEntry = Facilitator.create(user = 'ramsayb2',event = newEvent)

    testingEvent = Event.get(Event.eventName == "Test Event")

    addVolunteerToEvent('neillz', testingEvent.id, 2)

    username = "neillz"
    adminName = "ramsayb2"

    testingTrainingsExist = getTrainingTranscript(username)
    testingTrainingNotExist = getTrainingTranscript(adminName)


    assert testingTrainingNotExist.exists() == False
    assert testingTrainingsExist.exists()

    deleteEvent(2, testingEvent)
    assert Event.get_or_none(Event.id == testingEvent) is None

@pytest.mark.integration
def testingBonner():

    newEvent = Event.create(eventName = "Test Event",
                              term = 1,
                              description= "Event for testing",
                              timeStart = "18:00:00",
                              timeEnd = "21:00:00",
                              location = "The testing lab",
                              isRecurring = 0,
                              isRsvpRequired = 0,
                              isPrerequisiteForProgram = 0,
                              isTraining = 0,
                              isService = 0,
                              startDate =  2021-12-12,
                              endDate =  2021-12-13)

    programEvent = ProgramEvent.create(program=5, event=newEvent)

    facilitatorEntry = Facilitator.create(user = 'ramsayb2',event = newEvent)

    testingEvent = Event.get(Event.eventName == "Test Event")

    addVolunteerToEvent('neillz', testingEvent.id, 2)

    username = "neillz"
    adminName = "ramsayb2"

    testingBonnerExist = getBonnerScholarEvents(username)
    testingBonnerNotExist = getBonnerScholarEvents(adminName)


    assert testingBonnerNotExist.exists() == False
    assert testingBonnerExist.exists()

    deleteEvent(2, testingEvent)
    assert Event.get_or_none(Event.id == testingEvent) is None

@pytest.mark.integration
def testingSLCourses():

    username = "neillz"
    adminName = "ramsayb2"

    newCourse = Course.create(courseName = "Test Course",
                                term = 1,
                                status = 1,
                                courseCredit = "45",
                                createdBy = "totoro",
                                isAllSectionsServiceLearning = 0,
                                isPermanentlyDesignated = 0,
                                sectionBQuestion1 = "CharField()",
                                sectionBQuestion2 = "CharField()",
                                sectionBQuestion3 = "CharField()",
                                sectionBQuestion4 = "CharField()",
                                sectionBQuestion5 = "CharField()",
                                sectionBQuestion6 = "CharField()")

    testingCourse = Course.get(Course.courseName == "Test Course")

    courseParticipant = CourseParticipant.create(course = testingCourse.id,
                                                    user = username,
                                                    hoursEarned = 3.0)

    testingSLCExist = getSlCourseTranscript(username)
    testingSLCNotExist = getSlCourseTranscript(adminName)

    assert testingSLCExist.exists()
    assert testingSLCNotExist.exists() == False

    removeCourse = testingCourse.delete_instance(recursive = True, delete_nullable = True)
    assert Course.get_or_none(Course.id == testingCourse) is None

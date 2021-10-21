import pytest
from peewee import DoesNotExist

from app.logic.transcript import *
from app.models.user import User
from app.models.courseParticipant import CourseParticipant
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator
from app.logic.volunteers import addVolunteerToEvent
from app.logic.events import deleteEvent


@pytest.mark.integration
def testingTrainings():
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

    newEvent = Event.create(name = "Test Training Event",
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

    testingTrainingEvent = Event.get(Event.name == "Test Training Event")

    addVolunteerToEvent('namet', testingTrainingEvent.id, 2)

    username = "namet"
    adminName = "ramsayb2"

    testingTrainingsExist = getTrainingTranscript(username)
    testingTrainingNotExist = getTrainingTranscript(adminName)


    assert testingTrainingNotExist.exists() == False
    assert [event.event.name == "Test Training Event" for event in testingTrainingsExist]
    assert testingTrainingsExist.exists()



@pytest.mark.integration
def testingBonner():

    newEvent = Event.create(name = "Test Bonner Event",
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

    testingBonnerEvent = Event.get(Event.name == "Test Bonner Event")

    addVolunteerToEvent('namet', testingBonnerEvent.id, 2)

    username = "namet"
    adminName = "ramsayb2"

    testingBonnerExist = getBonnerScholarEvents(username)
    testingBonnerNotExist = getBonnerScholarEvents(adminName)


    assert testingBonnerNotExist.exists() == False
    assert [bonner.event.name == "Test Bonner Event" for bonner in testingBonnerExist]
    assert testingBonnerExist.exists()



@pytest.mark.integration
def testingSLCourses():

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

    testingSLCExist, instructorDict = getSlCourseTranscript(username)
    testingSLCNotExist, instructorDict = getSlCourseTranscript(adminName)

    assert testingSLCExist.exists()
    assert [slc.course.courseName == "Test Course" for slc in testingSLCExist]
    assert testingSLCNotExist.exists() == False

@pytest.mark.integration
def testingProgram():


    username = "namet"
    adminName = "ramsayb2"

    newEvent = Event.create(name = "Test Program Event",
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

    programEvent = ProgramEvent.create(program=1, event=newEvent)

    testingProgramEvent = Event.get(Event.name == "Test program Event")

    addVolunteerToEvent('namet', testingProgramEvent.id, 2)

    testingProgramExist = getProgramTranscript(username)
    testingProgramNotExist = getProgramTranscript(adminName)

    assert testingProgramNotExist.exists() == False
    assert [program.program.programName == "Test Program Event" for program in testingProgramExist]
    assert testingProgramExist.exists()



@pytest.mark.integration
def testingTotalHours():

    totalHours = getTotalHours("namet")

    assert totalHours == 9

    # delete training
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

from app.logic.minor import *
from peewee import *
from app.models.course import Course
from app.models.courseInstructor import CourseInstructor
from app.models import mainDB
from app.models.program import Program
from app.models.event import Event
from app.models.courseParticipant import CourseParticipant
from app.models.eventParticipant import EventParticipant
import pytest

@pytest.mark.integration
def test_getCourseInformation():
    with mainDB.atomic() as transaction:
        testCourse = Course.create(courseName="test get course information",
                      courseAbbreviation="TGCI",
                      sectionDesignation="something",
                      courseCredit=1.0,
                      term=3,
                      status=1,
                      createdBy="bledsoef",
                      serviceLearningDesignatedSections = "",
                      previouslyApprovedDescription="")
        
        testCourseInstructor = CourseInstructor.create(course=testCourse.id, user="bledsoef")
        
        courseInformation = getCourseInformation(testCourse.id)

        testCourseDict = model_to_dict(testCourse)

        manualCourseInformation = {"instructors":[testCourseInstructor.user.firstName + " " + testCourseInstructor.user.lastName], "course": testCourseDict}

        assert manualCourseInformation == courseInformation
        transaction.rollback()


@pytest.mark.integration
def test_updateMinorInterest():
    with mainDB.atomic() as transaction:
        test_user = User.create(
            username="FINN",
            firstName="Not",
            lastName="Yet",
            email=f"FINN@berea.edu",
            bnumber="B91111111")
        
        user = User.get_by_id("FINN")
        # make sure users have the default values of false and not interested, respectively
        assert user.minorInterest == False
        assert user.minorStatus == "No interest"
        updateMinorInterest("FINN")
        
        user = User.get_by_id("FINN")
        # make sure updateMinorInterest works correctly
        assert user.minorInterest == True
        assert user.minorStatus == "Interested"
        
        # verify unchecking box will restore defaults
        updateMinorInterest("FINN")
        
        user = User.get_by_id("FINN")  
        assert user.minorInterest == False
        assert user.minorStatus == "No interest"
        transaction.rollback()

@pytest.mark.integration
def test_getProgramEngagementHistory():
    with mainDB.atomic() as transaction:
        # create test objects
        test_user = User.create(
            username="FINN",
            firstName="Not",
            lastName="Yet",
            email=f"FINN@berea.edu",
            bnumber="B91111111")
        
        testingEvent = Event.create(name = "Testing event",
                                    term = 3,
                                    description = "This Event is Created to be tested.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = "2021-12-12",
                                    endDate = "2022-6-12",
                                    isCanceled = False,
                                    program = 2)
        
        # add the user as a participant of the event
        EventParticipant.create(user = test_user, event = testingEvent.id, hoursEarned=4.0)
        testingEvent = (Event.select(Event.id, Event.name, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
                                   .join(Program).switch()
                                   .join(EventParticipant)
                                   .where(EventParticipant.user == "FINN",
                                          Event.term == 3,
                                          Program.id == 2,
                                          Event.id == testingEvent)
                             )
        program = Program.get_by_id(2)

        # get the actual data from getProgramEngagementHistory
        actual_data = getProgramEngagementHistory(2, "FINN", 3)
        expected_data = {"program": program.programName, "events": [event for event in testingEvent.dicts()], "totalHours":4.0}
        assert actual_data == expected_data
        transaction.rollback()

@pytest.mark.integration
def test_getCommunityEngagementByTerm():
    with mainDB.atomic() as transaction:
        # create testing objects
        test_user = User.create(
            username="FINN",
            firstName="Not",
            lastName="Yet",
            email=f"FINN@berea.edu",
            bnumber="B91111111")
        
        testingEvent = Event.create(name = "Testing event",
                                    term = 2,
                                    description = "This Event is Created to be tested.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = "2021-12-12",
                                    endDate = "2022-6-12",
                                    isCanceled = False,
                                    program = 2)
        
        testCourse = Course.create(courseName="test get course information",
                      courseAbbreviation="TGCI",
                      sectionDesignation="something",
                      courseCredit=1.0,
                      term=3,
                      status=1,
                      createdBy="bledsoef",
                      serviceLearningDesignatedSections = "",
                      previouslyApprovedDescription="")
        # add the test_user as a participant in the course and event
        EventParticipant.create(user = test_user , event = testingEvent.id)
        CourseParticipant.create(course=testCourse, user=test_user, hoursEarned=1.0)

        course = Course.get_by_id(testCourse)
        event = Event.get_by_id(testingEvent)

        # write out what we expect the result to be
        expected_result = {("Summer 2021", 3):[{"name":course.courseName, "id":course.id, "type":"course", "term":course.term}], ("Spring 2021", 2):[{"name":event.program.programName, "id":event.program.id, "type":"program", "term":event.term}]}
        
        # get the actual result from getCommunityEngagementByTerm
        actual_result = dict(getCommunityEngagementByTerm("FINN"))

        assert actual_result == expected_result
        transaction.rollback()

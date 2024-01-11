import pytest
from peewee import *
from playhouse.shortcuts import model_to_dict
from collections import OrderedDict
from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.models.course import Course
from app.models.program import Program
from app.models.courseInstructor import CourseInstructor
from app.models.eventParticipant import EventParticipant
from app.models.courseParticipant import CourseParticipant
from app.models.individualRequirement import IndividualRequirement
from app.models.communityEngagementRequest import CommunityEngagementRequest
from app.logic.minor import getProgramEngagementHistory, getCourseInformation, updateMinorInterest, getCommunityEngagementByTerm, saveOtherEngagementRequest, getMinorInterest, getMinorProgress

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
        User.create(username="FINN",
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
        testUser = User.create(username="FINN",
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
        EventParticipant.create(user = testUser, event = testingEvent.id, hoursEarned=4.0)
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
        actualData = getProgramEngagementHistory(2, "FINN", 3)
        expectedData = {"program": program.programName, "events": [event for event in testingEvent.dicts()], "totalHours":4.0}
        assert actualData == expectedData
        transaction.rollback()

@pytest.mark.integration
def test_getCommunityEngagementByTerm():
    with mainDB.atomic() as transaction:
        # create testing objects
        testUser = User.create(username="FINN",
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
        
        # add the testUser as a participant in the course and event
        EventParticipant.create(user = testUser , event = testingEvent.id)
        CourseParticipant.create(course=testCourse, user=testUser, hoursEarned=1.0)

        course = Course.get_by_id(testCourse)
        event = Event.get_by_id(testingEvent)

        # write out what we expect the result to be
        expectedResult = OrderedDict({("Spring 2021", 2):[{"name":event.program.programName, "id":event.program.id, "type":"program", "term":event.term}],
                                       ("Summer 2021", 3):[{"name":course.courseName, "id":course.id, "type":"course", "term":course.term}]})
        
        # get the actual result from getCommunityEngagementByTerm
        actualResult = dict(getCommunityEngagementByTerm("FINN"))

        assert actualResult == expectedResult
        transaction.rollback()

@pytest.mark.integration
def test_saveOtherEngagementRequest():
    with mainDB.atomic() as transaction:
        testInfo = {'user': 'ramsayb2',
                    'experience': 'Test Experience',
                    'term': 3,
                    'description': 'Test Description',
                    'company': 'Test Company',
                    'hours': 5,
                    'weeks': 10,
                    'attachment': 'test_file.txt',
                    'status': 'Pending'
                   }

        # Save the requested event to the database
        saveOtherEngagementRequest(testInfo)

        expectedValues = {'user': testInfo['user'],
                           'experienceName': testInfo['experience'],
                           'term': testInfo['term'],
                           'description': testInfo['description'],
                           'company': testInfo['company'],
                           'weeklyHours': testInfo['hours'],
                           'weeks': testInfo['weeks'],
                           'filename': testInfo['attachment'],
                           'status': testInfo['status']
                          }

        # Get the actual saved request from the database (the most recent one)
        saved_request = CommunityEngagementRequest.select().order_by(CommunityEngagementRequest.id.desc()).first()

        # Check that the saved request matches the expected values
        for key, expectedValue in expectedValues.items():
            if key == "user":
                actualValue = 'ramsayb2'
            elif key == "term":
                actualValue = 3
            else:
                actualValue = getattr(saved_request, key)
            assert actualValue == expectedValue

        transaction.rollback()

@pytest.mark.integration
def test_getMinorInterest():
    with mainDB.atomic() as transaction: 
        # set every users minor interest to no interest
        User.update(minorStatus = 'No interest').where(User.minorStatus != 'No interest').execute()

        transaction.rollback()

@pytest.mark.integration
def test_getMinorProgress():
    with mainDB.atomic() as transaction: 
        # Make sure the individual requirement table is empty. 
        IndividualRequirement.delete().execute()
        noMinorProgress = getMinorProgress()

        assert noMinorProgress == []
        
        khattsSustainedEngagement = {"username": "khatts",
                                     "program": 2,
                                     "course": None,
                                     "description": None,
                                     "term": 3,
                                     "requirement": 14,
                                     "addedBy": "ramsayb2",
                                     "addedOn": "",
                                     }

        IndividualRequirement.create(**khattsSustainedEngagement)
        khattsProgress = getMinorProgress()
        
        assert khattsProgress[0]['engagementCount'] == 1
        assert khattsProgress[0]['hasSummer'] == 0

        khattsSummerEngagement = {"username": "khatts",
                                  "program": None,
                                  "course": None, 
                                  "description": "Summer engagement",
                                  "term": 3,
                                  "requirement": 16,
                                  "addedBy": "ramsayb2",
                                  "addedOn": ""
                                 }
        
        IndividualRequirement.create(**khattsSummerEngagement)
        khattsProgressWithSummer = getMinorProgress()

        assert khattsProgressWithSummer[0]['engagementCount']== 1
        assert khattsProgressWithSummer[0]['hasSummer'] == 1
        

        transaction.rollback()
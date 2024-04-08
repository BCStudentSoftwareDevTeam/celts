import pytest
from peewee import *
from collections import OrderedDict
from playhouse.shortcuts import model_to_dict

from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.event import Event
from app.models.course import Course
from app.models.program import Program
from app.models.courseInstructor import CourseInstructor
from app.models.eventParticipant import EventParticipant
from app.models.courseParticipant import CourseParticipant
from app.models.individualRequirement import IndividualRequirement
from app.models.communityEngagementRequest import CommunityEngagementRequest
from app.logic.minor import saveSummerExperience, saveOtherEngagementRequest, getMinorInterest, getMinorProgress, setCommunityEngagementForUser, removeSummerExperience
from app.logic.minor import getProgramEngagementHistory, getCourseInformation, toggleMinorInterest, getCommunityEngagementByTerm, getSummerExperience, getSummerTerms, getEngagementTotal

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
def test_toggleMinorInterest():
    with mainDB.atomic() as transaction:
        User.create(username="FINN",
                    firstName="Not",
                    lastName="Yet",
                    email="FINN@berea.edu",
                    bnumber="B91111111")
        
        user = User.get_by_id("FINN")
        # make sure users have the default values of false and not interested, respectively
        assert user.minorInterest == False
        toggleMinorInterest("FINN")
        
        user = User.get_by_id("FINN")
        # make sure toggleMinorInterest works correctly
        assert user.minorInterest == True
        
        # verify unchecking box will restore defaults
        toggleMinorInterest("FINN")
        
        user = User.get_by_id("FINN")  
        assert user.minorInterest == False
        transaction.rollback()

@pytest.mark.integration
def test_getProgramEngagementHistory():
    with mainDB.atomic() as transaction:
        # create test objects
        testUser = User.create(username="FINN",
                                firstName="Not",
                                lastName="Yet",
                                email="FINN@berea.edu",
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
                               email="FINN@berea.edu",
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
        expectedResult = OrderedDict({
                ("Spring 2021", 2):[{"name":event.program.programName, "id":event.program.id, "type":"program", "matched": False, "term":event.term.id}],
                ("Summer 2021", 3):[{"name":course.courseName, "id":course.id, "type":"course", "matched": False, "term":course.term.id}]})
        
        # get the actual result from getCommunityEngagementByTerm
        actualResult = getCommunityEngagementByTerm("FINN")
        assert actualResult == expectedResult

        transaction.rollback()

    # check that our total function works
    assert 0 == getEngagementTotal(actualResult)

    actualResult[("Spring 2021", 2)][0]["matched"] = True
    assert 1 == getEngagementTotal(actualResult)

    actualResult[("Summer 2021", 3)].append({"matched":True})
    assert 2 == getEngagementTotal(actualResult)

@pytest.mark.integration
def test_saveOtherEngagementRequest():
    with mainDB.atomic() as transaction:
        testInfo = {'user': 'ramsayb2',
                    'experienceName': 'Test Experience',
                    'term': 3,
                    'description': 'Test Description',
                    'company': 'Test Company',
                    'weeklyHours': 5,
                    'weeks': 10,
                    'filename': 'test_file.txt',
                   }

        # Save the requested event to the database
        saveOtherEngagementRequest(testInfo)

        expectedValues = {'user': testInfo['user'],
                           'experienceName': testInfo['experienceName'],
                           'term': testInfo['term'],
                           'description': testInfo['description'],
                           'company': testInfo['company'],
                           'weeklyHours': testInfo['weeklyHours'],
                           'weeks': testInfo['weeks'],
                           'filename': testInfo['filename'],
                           'status': "Pending"
                          }

        # Get the actual saved request from the database (the most recent one)
        savedRequest = CommunityEngagementRequest.select().order_by(CommunityEngagementRequest.id.desc()).first()
        # Check that the saved request matches the expected values
        for key, expectedValue in expectedValues.items():
            if key == "user":
                assert savedRequest.user.username == 'ramsayb2'
            elif key == "term":
                assert savedRequest.term.id == 3
            else:             
                assert getattr(savedRequest, key) == expectedValue

        transaction.rollback()

@pytest.mark.integration
def test_setCommunityEngagementForUser():
    with mainDB.atomic() as transaction: 
        IndividualRequirement.delete().execute()

        # Adding requirement
        khattsEngagementData1 = {"id": 2,
                                "matched": False, 
                                "name": 'Spanish Help',
                                'term': 2,
                                "type": 'course',
                                'username': 'khatts'}
        
        khattsEngagementData2 = {"id": 9,
                                "matched": False, 
                                "name": 'CELTS-Sponsored Event',
                                'term': 3,
                                "type": 'program',
                                'username': 'khatts'}
        
        khattsEngagementData3 = {"id": 6,
                                "matched": False, 
                                "name": 'Habitat For Humanity',
                                'term': 2,
                                "type": 'program',
                                'username': 'khatts'}
        
        khattsEngagementData4 = {"id": 4,
                                "matched": False, 
                                "name": 'People Who Care',
                                'term': 3,
                                "type": 'program',
                                'username': 'khatts'}
        
        khattsEngagementData5 = {"id": 1,
                                "matched": False, 
                                "name": 'Databses',
                                'term': 2,
                                "type": 'course',
                                'username': 'khatts'}
        
        neillzEngagementData1 = {"id": 4,
                                "matched": False, 
                                "name": 'People Who Care',
                                'term': 3,
                                "type": 'program',
                                'username': 'neillz'}
        
        neillzEngagementData2 = {"id": 1,
                                "matched": False, 
                                "name": 'Databses',
                                'term': 2,
                                "type": 'course',
                                'username': 'neillz'}
        
        setCommunityEngagementForUser('add', khattsEngagementData1, 'ramsayb2')
        
        allStudentReq = IndividualRequirement.select()
        # get count 
        allStudentReq.count() == 1
        assert allStudentReq[0].course == Course.get_by_id(2)
        assert allStudentReq[0].program == None

        # add 4 more engagements and make sure the 5th raises the expected exception 
        setCommunityEngagementForUser('add', khattsEngagementData2, 'ramsayb2')
        setCommunityEngagementForUser('add', khattsEngagementData3, 'ramsayb2')
        setCommunityEngagementForUser('add', khattsEngagementData4, 'ramsayb2')

        with pytest.raises(DoesNotExist):
            setCommunityEngagementForUser('add', khattsEngagementData5, 'ramsayb2')


        # add records for another student and make sure it is added correctly. 
        setCommunityEngagementForUser('add', neillzEngagementData1, 'ramsayb2')
        allStudentReq = IndividualRequirement.select()
        assert allStudentReq.count() == 5
        assert allStudentReq[4].username_id == 'neillz'

        # add a second record for that other student.
        setCommunityEngagementForUser('add', neillzEngagementData2, 'ramsayb2')
        allStudentReq = IndividualRequirement.select()
        assert allStudentReq.count() == 6
        assert allStudentReq[3].username_id == 'khatts'
        assert allStudentReq[4].username_id == 'neillz'
        assert allStudentReq[4].course == None
        assert allStudentReq[5].username_id == 'neillz'
        assert allStudentReq[5].course == Course.get_by_id(1)

        # Removing requirement
        setCommunityEngagementForUser('remove', khattsEngagementData1, 'ramsayb2')
        allStudentReq = list(IndividualRequirement.select())
        assert allStudentReq[0].course == None
        assert allStudentReq[0].program == Program.get_by_id(9)
        
        transaction.rollback()



@pytest.mark.integration
def test_getMinorInterest():
    with mainDB.atomic() as transaction: 
        # set every users minor interest to no interest
        User.update(minorInterest = 0).where(User.minorInterest == 1).execute()
        noStudentsInterested = getMinorInterest()
        assert noStudentsInterested == []

        # Add a student who has progress towards the minor. They should not be in returned list
        User.update(minorInterest = 1).where(User.username == 'khatts').execute()
        minorInterest = getMinorInterest()
        assert minorInterest == []
       
       # Add a student will be returned in the list
        User.update(minorInterest = 1).where(User.username == 'partont').execute()
        oneStudentInterested = getMinorInterest()
        assert len(oneStudentInterested) == 1
        oneStudentInterested[0]['username'] == 'partont'

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
        minorProgress = getMinorProgress()
        sreynitProgress = minorProgress[0]
        assert sreynitProgress['engagementCount'] == 1
        assert sreynitProgress['hasSummer'] == "Incomplete"
        assert sreynitProgress['hasCommunityEngagementRequest'] == 0

        khattsSummerEngagement = {"username": "khatts",
                                  "program": None,
                                  "course": None, 
                                  "description": "Summer engagement",
                                  "term": 3,
                                  "requirement": 16,
                                  "addedBy": "ramsayb2",
                                  "addedOn": "",
                                 }
        khattsRequestedEngagement = {"user": "khatts",
                                     "experienceName ": "Voluteering",
                                     "company" : "Berea Celts",
                                     "term": 3,
                                     "description": "Summer engagement",
                                     "weeklyHours": 3,
                                     "weeks": 4,
                                     "filename": None,
                                     "status" : "Pending",
                                    }
    
        CommunityEngagementRequest.create(**khattsRequestedEngagement)
        IndividualRequirement.create(**khattsSummerEngagement)
        minorProgressWithSummerAndRequestOther = getMinorProgress()
        sreynitProgress = minorProgressWithSummerAndRequestOther[0]
        assert sreynitProgress['engagementCount']== 1
        assert sreynitProgress['hasSummer'] == "Completed"
        assert sreynitProgress['hasCommunityEngagementRequest'] == 1

        transaction.rollback()

@pytest.mark.integration
def test_saveSummerExperience():
    with mainDB.atomic() as transaction: 
        IndividualRequirement.delete().execute()

        # Add summer Experience for a user 
        partontSummerExperience = {"summerExperience": "Test Summer Experience for Tyler", "selectedSummerTerm": "Summer 2021"}
        
        saveSummerExperience('partont', partontSummerExperience, 'ramsayb2')

        allStudentReq = IndividualRequirement.select()
        assert allStudentReq.count() == 1
        assert allStudentReq[0].username_id == 'partont'
        assert allStudentReq[0].description == 'Test Summer Experience for Tyler'

        # Add a second summer engagement for the same user. The expected behavior is the engagement that was put in first 
        # should be deleted and the only entry is new one

        newPartontSummerExperience = {"summerExperience": "Second Summer Experience for Tyler", "selectedSummerTerm": "Summer 2021"}
        
        saveSummerExperience('partont', newPartontSummerExperience, 'ramsayb2')

        allStudentReq = IndividualRequirement.select()
        assert allStudentReq.count() == 1
        assert allStudentReq[0].username_id == 'partont'
        assert allStudentReq[0].description == 'Second Summer Experience for Tyler'

        # Add a summer experience for another studnet and verify both students have summer experience records
        
        neillzSummerExperience = {"summerExperience": "Summer Experience for Zach", "selectedSummerTerm": "Summer 2021"}
        saveSummerExperience('neillz', neillzSummerExperience, 'ramsayb2')
        allStudentReq = IndividualRequirement.select()
        assert allStudentReq.count() == 2
        assert allStudentReq[0].username_id == 'partont'
        assert allStudentReq[1].username_id == 'neillz'
        assert allStudentReq[1].description == "Summer Experience for Zach"

        transaction.rollback()

@pytest.mark.integration
def test_getSummerExperience():
    with mainDB.atomic() as transaction:
        IndividualRequirement.delete().execute()

        partontSummerEngagement = {"username": "partont",
                                   "program": None,
                                   "course": None, 
                                   "description": "Summer engagement",
                                   "term": 3,
                                   "requirement": 16,
                                   "addedBy": "ramsayb2",
                                   "addedOn": ""
                                  }
        IndividualRequirement.create(**partontSummerEngagement)
        tylerSummerEngagement = getSummerExperience('partont')

        assert tylerSummerEngagement[1] == "Summer engagement"
        
        IndividualRequirement.update(description = "Updated summer engagement").where(IndividualRequirement.username == 'partont').execute()
        tylerUpdatedSummerEngagement = getSummerExperience('partont')

        assert tylerUpdatedSummerEngagement[1] == "Updated summer engagement"
        
        IndividualRequirement.update(term = 6).where(IndividualRequirement.username == 'partont').execute()
        tylerUpdatedSummerEngagementTerm = getSummerExperience('partont')

        assert tylerUpdatedSummerEngagementTerm[0] == 'Summer 2022'

        transaction.rollback()

@pytest.mark.integration
def test_removeSummerExperience():
    with mainDB.atomic() as transaction:
        # remove the summer experience for khatts that is in test data

        removeSummerExperience('khatts')

        khattsNoSummerExperience = list(IndividualRequirement.select()
                                                             .where(IndividualRequirement.username == 'khatts',
                                                                    IndividualRequirement.description.is_null(False)))

        assert khattsNoSummerExperience == []

        transaction.rollback()

@pytest.mark.integration
def test_getSummerTerms():
    with mainDB.atomic() as transaction:
        # get all the terms that have the isSummer flag that are in test data
        baseSummerTerms = getSummerTerms()

        assert len(list(baseSummerTerms)) == 2

        Term.update(isSummer = 0).where(Term.isSummer == 1).execute()
        noSummerTerms = getSummerTerms()

        assert len(list(noSummerTerms)) == 0

        transaction.rollback()

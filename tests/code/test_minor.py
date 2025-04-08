import pytest
import os
import uuid
from peewee import *
from flask import g
from collections import OrderedDict
from playhouse.shortcuts import model_to_dict
from werkzeug.datastructures import ImmutableMultiDict
from app import app

from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.event import Event
from app.models.course import Course
from app.models.program import Program
from app.models.courseInstructor import CourseInstructor
from app.models.eventParticipant import EventParticipant
from app.models.cceMinorProposal import CCEMinorProposal
from app.models.courseParticipant import CourseParticipant
from app.models.individualRequirement import IndividualRequirement
from app.models.attachmentUpload import AttachmentUpload
from app.logic.minor import createOtherEngagementRequest, getMinorInterest, getMinorProgress, setCommunityEngagementForUser, createSummerExperience, removeProposal
from app.logic.minor import getProgramEngagementHistory, getCourseInformation, toggleMinorInterest, getCommunityEngagementByTerm, getSummerExperience, getEngagementTotal, getCCEMinorProposals
<<<<<<< HEAD
from app.logic.fileHandler import FileHandler
from werkzeug.datastructures import FileStorage

=======
from app.logic.minor import declareMinorInterest, getDeclaredMinorStudents
>>>>>>> 1e270f70da842b6140997d186b86138684acfbf3

@pytest.fixture
def testUser(request):
    """Fixture to create a user"""
    params = getattr(request, "param", {})
    newUser = User.create(
        username=params.get("username", f"bledsoef{uuid.uuid4().hex[:8]}"), # create a random username to make sure there are no conflicts with duplicates
        firstName=params.get("firstName", "Fin"),
        lastName=params.get("lastName", "Bledso"),
        email=params.get("email", "bledsoefin@gmail.com"),
        bnumber=params.get("bnumber", f"B{uuid.uuid4().hex[:8]}"),
    )
    yield newUser
    newUser.delete_instance()

@pytest.fixture
def testTerm(request):
    """Fixture to create a term."""
    params = getattr(request, "param", {})
    newTerm = Term.create(
        description=params.get("description", "Summer 2025"),
        year=params.get("year", 2025),
        academicYear=params.get("academicYear", "2024-2025"),
        isSummer=params.get("isSummer", 1),
        isCurrentTerm=params.get("isCurrentTerm", 0)
    )

    yield newTerm
    newTerm.delete_instance() 

@pytest.fixture
def testProposal(request):
    """Fixture to create form data for CCEMinorProposals."""
    params = getattr(request, "param", {})
    proposalType = params.get("proposalType", "summerExperience")
    if proposalType == "summerExperience":
        defaultProposal = {
            "term": params.get("term", 3),
            "roleDescription": params.get("roleDescription", "Assistant to Finn"),
            "experienceType": params.get("experienceType", "Internship"),
            "contentArea": params.get("contentArea", ["Power and inequality", "Civic literacy"]),
            "orgName": params.get("orgName", "Finn's Org"),
            "orgAddress":  params.get("orgAddress", "Finn's House"),
            "orgPhone": params.get("orgPhone", "513-384-FINN"),
            "orgWebsite": params.get("orgWebsite" ,"www.finn.com"),
            "supervisorName": params.get("supervisorName", "Kafui Gle"),
            "supervisorPhone": params.get("supervisorPhone", "513-226-GLEK"),
            "supervisorEmail": params.get("supervisorEmail", "kafuigle.com"),
            'totalHours': params.get("totalHours", 300),
            'totalWeeks': params.get("totalWeeks", 10),
        }
    else:
        defaultProposal = {
            "term": params.get("term", 3),
            "experienceName": params.get("experienceName", "Assistant to Finn"),
            "experienceType": params.get("experienceType", "Internship"),
            "contentArea": params.get("contentArea", ["Power and inequality", "Civic literacy"]),
            "orgName": params.get("orgName", "Finn's Org"),
            "orgAddress":  params.get("orgAddress", "Finn's House"),
            "orgPhone": params.get("orgPhone", "513-384-FINN"),
            "orgWebsite": params.get("orgWebsite" ,"www.finn.com"),
            "supervisorName": params.get("supervisorName", "Kafui Gle"),
            "supervisorPhone": params.get("supervisorPhone", "513-226-GLEK"),
            "supervisorEmail": params.get("supervisorEmail", "kafuigle.com"),
            'totalHours': params.get("totalHours", 300),
            'totalWeeks': params.get("totalWeeks", 10),
            'experienceDescription': params.get("experienceDescription", "Working day and night to make sure Finn's needs are met"),
        } 
    # override default values with those put in the parameters.
    return defaultProposal

@pytest.mark.integration
def test_getCourseInformation(testUser):
    with mainDB.atomic() as transaction:
        testCourse = Course.create(courseName="test get course information",
                                   courseAbbreviation="TGCI",
                                   sectionDesignation="something",
                                   courseCredit=1.0,
                                   term=3,
                                   status=1,
                                   createdBy=testUser.username,
                                   serviceLearningDesignatedSections = "",
                                   previouslyApprovedDescription="")
        
        testCourseInstructor = CourseInstructor.create(course=testCourse.id, user=testUser.username)
        
        courseInformation = getCourseInformation(testCourse.id)

        testCourseDict = model_to_dict(testCourse)

        manualCourseInformation = {"instructors":[testCourseInstructor.user.firstName + " " + testCourseInstructor.user.lastName], "course": testCourseDict}

        assert manualCourseInformation == courseInformation
        transaction.rollback()


@pytest.mark.integration
def test_toggleMinorInterest(testUser):
    with mainDB.atomic() as transaction:
        # make sure users have the default values of false and not interested, respectively
        assert testUser.minorInterest == False
        toggleMinorInterest(testUser.username, True)
        
        testUser = User.get_by_id(testUser.username)
        # make sure toggleMinorInterest works correctly
        assert testUser.minorInterest == True
        
        # verify unchecking box will restore defaults
        toggleMinorInterest(testUser.username, False)
        
        testUser = User.get_by_id(testUser.username)
        assert testUser.minorInterest == False
        transaction.rollback()

@pytest.mark.integration
def test_getProgramEngagementHistory(testUser):
    with mainDB.atomic() as transaction:
        # create test objects
        testingEvent = Event.create(name = "Testing event",
                                    term = 3,
                                    description = "This Event is Created to be tested.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 1,
                                    startDate = "2021-12-12",
                                    isCanceled = False,
                                    program = 2)
        
        # add the user as a participant of the event
        EventParticipant.create(user = testUser, event = testingEvent.id, hoursEarned=4.0)
        testingEvent = (Event.select(Event.id, Event.name, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
                             .join(Program).switch()
                             .join(EventParticipant)
                             .where(EventParticipant.user == testUser.username,
                                    Event.term == 3,
                                    Program.id == 2,
                                    Event.id == testingEvent)
                                    )
        program = Program.get_by_id(2)

        # get the actual data from getProgramEngagementHistory
        actualData = getProgramEngagementHistory(2, testUser.username, 3)
        expectedData = {"program": program.programName, "events": [event for event in testingEvent.dicts()], "totalHours":4.0}
        assert actualData == expectedData
        transaction.rollback()

@pytest.mark.integration
@pytest.mark.parametrize("testProposal", [
    {"proposalType": "otherEngagement"},
    {"proposalType": "summerExperience"},
 
], indirect=True)
def test_getCCEMinorProposals(testUser, testProposal):

    with mainDB.atomic() as transaction:

        assert getCCEMinorProposals(testUser.username) == []

        with app.app_context():
            g.current_user = testUser.username
            createOtherEngagementRequest(testUser.username, testProposal)

        assert len(getCCEMinorProposals(testUser.username)) == 1
        
        with app.app_context():
            g.current_user = testUser.username
            createSummerExperience(testUser.username, ImmutableMultiDict(testProposal))

        assert len(getCCEMinorProposals(testUser.username)) == 2
        
        summerExperienceCount = 0
        otherExperienceCount = 0
        for experience in getCCEMinorProposals(testUser.username):
            if experience["type"] == "Summer Experience":
                summerExperienceCount+=1
            elif experience["type"] == "Other Engagement":
                otherExperienceCount+=1
            else:
                raise AssertionError
            
        assert summerExperienceCount == 1
        assert otherExperienceCount == 1

        transaction.rollback()
    


@pytest.mark.integration
def test_getCommunityEngagementByTerm(testUser):
    with mainDB.atomic() as transaction:
        # create testing objects   

        testingServiceEvent = Event.create(name = "Testing event",
                                    term = 1, # Fall 2020
                                    description = "This Service Event is Created to be tested.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 1,
                                    startDate = "2021-12-12",
                                    isCanceled = False,
                                    program = 1)        
        
        testCourse = Course.create(courseName="test get course information",
                                   courseAbbreviation="TGCI",
                                   sectionDesignation="something",
                                   courseCredit=1.0,
                                   term=3, # Summer 2021
                                   status=1,
                                   createdBy="bledsoef",
                                   serviceLearningDesignatedSections = "",
                                   previouslyApprovedDescription="")
 
        # add the testUser as a participant in the course and event
        EventParticipant.create(user = testUser , event = testingServiceEvent.id)
        CourseParticipant.create(course=testCourse, user=testUser, hoursEarned=1.0)

        # get the service event and course
        serviceCourse = Course.get_by_id(testCourse)
        serviceEvent = Event.get_by_id(testingServiceEvent)

        # write out what we expect the result to be as the getCommunityEngagementByTerm is suppose to return name, id, type, matched and term
        expectedServiceResult = OrderedDict({
                ("Fall 2020", 1):[{"name":serviceEvent.program.programName, "id":serviceEvent.program.id, "type":"program", "matched": False, "term":serviceEvent.term.id}],
                ("Summer 2021", 3):[{"name":serviceCourse.courseName, "id":serviceCourse.id, "type":"course", "matched": False, "term":serviceCourse.term.id}]})
        
        # get the actual result from getCommunityEngagementByTerm
        actualServiceResult = getCommunityEngagementByTerm(testUser.username)

        assert actualServiceResult == expectedServiceResult
        transaction.rollback()

    with mainDB.atomic() as transaction:
        
        testingNonServiceEvent = Event.create(name = "Testing non-service event",
                                    term = 2,
                                    description = "This Non-Service Event is Created to be tested.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = "2021-1-1",
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
        EventParticipant.create(user = testUser , event = testingNonServiceEvent.id)
        CourseParticipant.create(course=testCourse, user=testUser, hoursEarned=1.0)

        # get the non-service event and course
        nonServiceCourse = Course.get_by_id(testCourse)
        nonServiceEvent = Event.get_by_id(testingNonServiceEvent)

        #This expected result is without the non-service event as the return value of getCommunityEngagementByTerm 
        #is suppose to return name, id, type, matched and term of events with only isService as True
        expectedNonServiceResult = OrderedDict({
            ("Summer 2021", 3):[{"name":nonServiceCourse.courseName, "id":nonServiceCourse.id, "type":"course", "matched": False, "term":nonServiceCourse.term.id}]})
        
        #This expected result is with the non-service event to test whether getCommunityEngagementByTerm is actualy returning only service events and courses
        unexpectedResultWithoutServiceEvent = OrderedDict({
            ("Spring 2021", 2):[{"name":nonServiceEvent.program.programName, "id":nonServiceEvent.program.id, "type":"program", "matched": False, "term":nonServiceEvent.term.id}],
            ("Summer 2021", 3):[{"name":nonServiceCourse.courseName, "id":nonServiceCourse.id, "type":"course", "matched": False, "term":nonServiceCourse.term.id}]})
        
        # get the actual result from getCommunityEngagementByTerm
        actualNonServiceResult = getCommunityEngagementByTerm(testUser.username)

        assert actualNonServiceResult == expectedNonServiceResult
        assert actualNonServiceResult != unexpectedResultWithoutServiceEvent
        transaction.rollback()

    # check that our total function works
    assert 0 == getEngagementTotal(actualServiceResult)
    
    # add a matched event to the service result and check the total
    actualServiceResult[("Fall 2020", 1)][0]["matched"] = True
    assert 1 == getEngagementTotal(actualServiceResult)

    # add a matched event to the service result and check the total
    actualServiceResult[("Summer 2021", 3)].append({"matched":True})
    assert 2 == getEngagementTotal(actualServiceResult)
    assert 0 == getEngagementTotal(actualNonServiceResult)

    # add a matched event to the service result and check the total
    actualNonServiceResult[("Summer 2021", 3)].append({"matched":True})
    assert 1 == getEngagementTotal(actualNonServiceResult)

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
        
        # create a sustained engagement for Sreynit
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
        assert sreynitProgress['hasCCEMinorProposal'] == 0

        # add a summer engagement and requested engagement to Sreynit's progress


        khattsSummerExperience = ImmutableMultiDict({
            "term": 3,
            "roleDescription": "Assistant to Finn",
            "experienceType": "Internship",
            "contentArea": ["Power and inequality", "Civic literacy"],
            "orgName": "Finn's Org",
            "orgAddress": "Finn's House",
            "orgPhone": "513-384-FINN",
            "orgWebsite": "www.finn.com",
            "supervisorName": "Finn",
            "supervisorPhone": "513-384-FINN",
            "supervisorEmail": "finn@finn.com",
        })
   
        khattsRequestedEngagement = ({'term': 3,
                    'experienceName': 'Test Experience',
                    'orgName': 'Test Company',
                    'orgAddress': '123 test ln',
                    'orgPhone': '(123)-456-7890',
                    'orgPhone': '(123)-456-7890',
                    'orgWebsite': "kafui.com",
                    'supervisorPhone': '(123)-798-3516',
                    'supervisorName': 'kafui',
                    'supervisorEmail': 'test@supervisor.com',
                    'totalHours': 300,
                    'totalWeeks': 10,
                    'experienceDescription': 'Test Description',
        })
        
        # verify that Sreynit has a summer, 1 engagement, and an other community engagement request in
        with app.app_context():
            g.current_user = "ramsayb2"
            createOtherEngagementRequest("khatts", khattsRequestedEngagement)
            createSummerExperience("khatts", khattsSummerExperience)

        minorProgressWithSummerAndRequestOther = getMinorProgress()
        sreynitProgress = minorProgressWithSummerAndRequestOther[0]
        assert sreynitProgress['engagementCount'] == 1
        assert sreynitProgress['hasSummer'] == "Completed"
        assert sreynitProgress['hasCCEMinorProposal'] == 1

        transaction.rollback()

@pytest.mark.integration
def test_createSummerExperience(testUser, testTerm, testProposal):
    with mainDB.atomic() as transaction:
        # create testing objects
        
        testProposal["term"] = testTerm

        User.create(username="glek",
                    firstName="kafui",
                    lastName="gle",
                    email="kaf@berea.edu",
                    bnumber="B91111113")
        
        # verify FINN has no summer experiences in currently
        initialSummerExperiences = list(CCEMinorProposal.select().where(CCEMinorProposal.student == testUser.username, CCEMinorProposal.proposalType == 'Summer Experience'))

        assert len(initialSummerExperiences) == 0

        # create the summer experience with the test data and verify FINN has a new entry
        with app.app_context():
            g.current_user = "glek"
            createSummerExperience(testUser.username, ImmutableMultiDict(testProposal))

        newSummerExperiences = list(CCEMinorProposal.select().where(CCEMinorProposal.student == testUser.username, CCEMinorProposal.proposalType == 'Summer Experience'))
        assert len(newSummerExperiences) == 1

        assert newSummerExperiences[0].createdBy.username == "glek"
        
        transaction.rollback()

@pytest.mark.parametrize("testProposal", [
    {"proposalType": "otherEngagement"}
], indirect=True)
@pytest.mark.integration
def test_createOtherEngagementRequest(testUser, testProposal):
    with mainDB.atomic() as transaction:
        User.create(username="glek",
                    firstName="kafui",
                    lastName="gle",
                    email="kaf@berea.edu",
                    bnumber="B91111113")
        
        # Save the requested event to the database
        with app.app_context():
            g.current_user = "glek"
            createOtherEngagementRequest(testUser.username, testProposal)

        # Get the actual saved request from the database (the most recent one)
        initialOtherExperiences = CCEMinorProposal.select().where(CCEMinorProposal.proposalType == 'Other Engagement', CCEMinorProposal.student == testUser.username)
       
        assert len(initialOtherExperiences) == 1 

        transaction.rollback()

@pytest.mark.parametrize("testProposal", [
    {"proposalType": "otherEngagement"}
], indirect=True)
@pytest.mark.integration
def test_removeProposal(testProposal, testUser):
    '''creates a test course with all foreign key fields. tests if they can
    be deleted'''

    testProposalId = 999

    with mainDB.atomic() as transaction:

        assert list(CCEMinorProposal.select(CCEMinorProposal.id).where(CCEMinorProposal.id == testProposalId)) == []


        testOtherEngagement = CCEMinorProposal.create(id=testProposalId,
                                student = testUser.username,
                                proposalType = 'Other Engagement',
                                createdBy = testUser.username,
                                status = 'Pending',
                                **testProposal
                            )
        assert list(CCEMinorProposal.select().where(CCEMinorProposal.id == testProposalId)) == [testOtherEngagement]

        # creates a base object for proposal events 
        proposalFileStorageObject = [FileStorage(filename= "proposal.pdf")]

        handledProposalFile = FileHandler(proposalFileStorageObject, proposalId=testProposalId)

        # uploading a file to proposalattachments 
        handledProposalFile.saveFiles()
        
        try:
            assert AttachmentUpload.select().where(AttachmentUpload.proposal_id == testProposalId, AttachmentUpload.fileName == f"{testProposalId}.pdf").exists()
            assert 1 == AttachmentUpload.select().where(AttachmentUpload.proposal_id == testProposalId, AttachmentUpload.fileName == f"{testProposalId}.pdf").count()
            
            with app.app_context():
                g.current_user = testUser.username
                removeProposal(testProposalId)

            assert list(CCEMinorProposal.select().where(CCEMinorProposal.id == testProposalId)) == []
        
            assert not AttachmentUpload.select().where(AttachmentUpload.proposal_id == testProposalId, AttachmentUpload.fileName == f"{testProposalId}.pdf").exists()
            assert 0 == AttachmentUpload.select().where(AttachmentUpload.proposal_id == testProposalId, AttachmentUpload.fileName == f"{testProposalId}.pdf").count()

        except Exception as e:
            raise e 
        
        finally:
            fileExists = AttachmentUpload.get_or_none(proposal_id = testProposalId)
            fullFilePath = handledProposalFile.getFileFullPath(f'{testProposalId}.pdf')
            if fileExists:
                os.remove(fullFilePath)

        transaction.rollback()
        
@pytest.mark.integration
def test_declareMinorInterest():
    
    with mainDB.atomic() as transaction:
        # Get three students with interest in minor
        student1 = User.get_by_id("agliullovak")
        student2 = User.get_by_id("partont")
        student3 = User.get_by_id("bryanta")
        
        assert student1.declaredMinor == False
        assert student2.declaredMinor == False
        assert student3.declaredMinor == False
        
        # Declare students interested in minor
        declareMinorInterest("agliullovak")
        declareMinorInterest("partont")
        declareMinorInterest("bryanta")
        
        student1 = User.get_by_id("agliullovak")
        student2 = User.get_by_id("partont")
        student3 = User.get_by_id("bryanta")
        
        assert student1.declaredMinor == True
        assert student2.declaredMinor == True
        assert student3.declaredMinor == True
        
        # Undeclare students
        declareMinorInterest("agliullovak")
        declareMinorInterest("partont")
        declareMinorInterest("bryanta")
        
        student1 = User.get_by_id("agliullovak")
        student2 = User.get_by_id("partont")
        student3 = User.get_by_id("bryanta")
        
        assert student1.declaredMinor == False
        assert student2.declaredMinor == False
        assert student3.declaredMinor == False
        
        transaction.rollback()


@pytest.mark.integration
def test_getDeclaredMinorStudents():
    
    with mainDB.atomic() as transaction:
        # Get all the declared students
        declaredStudents = getDeclaredMinorStudents()
        
        assert declaredStudents == []
        assert len(declaredStudents) == 0
        
        student1 = User.get_by_id("agliullovak")
        student2 = User.get_by_id("partont")
        student3 = User.get_by_id("bryanta")
        
        assert student1.declaredMinor == False
        assert student2.declaredMinor == False
        assert student3.declaredMinor == False
        
        student1.declaredMinor = True
        student2.declaredMinor = True
        student3.declaredMinor = True
        
        student1.save()
        student2.save()
        student3.save()
        
        # Get all the declared students after recent changes
        newDeclaredStudents = getDeclaredMinorStudents()
        
        assert len(newDeclaredStudents) == 3
        
        transaction.rollback()

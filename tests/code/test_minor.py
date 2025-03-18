import pytest
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
from app.logic.fileHandler import FileHandler
from werkzeug.datastructures import FileStorage


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
                                    isService = 1,
                                    startDate = "2021-12-12",
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
def test_getCCEMinorProposals():

    


    getCCEMinorProposals("ayisie")



@pytest.mark.integration
def test_getCommunityEngagementByTerm():
    with mainDB.atomic() as transaction:
        # create testing objects  
        testUser = User.create(username="FINN",
                    firstName="Not",
                    lastName="Yet",
                    email="FINN@berea.edu",
                    bnumber="B91111111")   
        
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
        actualServiceResult = getCommunityEngagementByTerm("FINN")

        assert actualServiceResult == expectedServiceResult
        transaction.rollback()

    with mainDB.atomic() as transaction:
        # create testing objects
        testUser = User.create(username="FINN",
                    firstName="Not",
                    lastName="Yet",
                    email="FINN@berea.edu",
                    bnumber="B91111111")
            
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
        actualNonServiceResult = getCommunityEngagementByTerm("FINN")

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
def test_createSummerExperience():
    with mainDB.atomic() as transaction:
        # create testing objects
        User.create(username="FINN",
                    firstName="Not",
                    lastName="Yet",
                    email="FINN@berea.edu",
                    bnumber="B91111111")
        
        User.create(username="glek",
                    firstName="kafui",
                    lastName="gle",
                    email="kaf@berea.edu",
                    bnumber="B91111113")
        
        newTerm = Term.create(description="Summer 2025",
            year=2025,
            academicYear="2024-2025",
            isSummer=1,
            isCurrentTerm=0)
        
        testFormData1 = ImmutableMultiDict({
            "term": newTerm,
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

        testFormData2 = ImmutableMultiDict({
            "term": newTerm,
            "roleDescription": "Assistant to Finn",
            "experienceType": "Some other experience type",
            "contentArea": ["Power and inequality", "Civic literacy"],
            "orgName": "Finn's Org",
            "orgAddress": "Finn's House",
            "orgPhone": "513-384-FINN",
            "orgWebsite": "www.finn.com",
            "supervisorName": "Finn",
            "supervisorPhone": "513-384-FINN",
            "supervisorEmail": "finn@finn.com",
        })
        
        # verify FINN has no summer experiences in currently
        initialSummerExperiences = list(CCEMinorProposal.select().where(CCEMinorProposal.student == "FINN", CCEMinorProposal.proposalType == 'Summer Experience'))

        assert len(initialSummerExperiences) == 0

        # create the summer experience with the test data and verify FINN has a new entry
        with app.app_context():
            g.current_user = "glek"
            createSummerExperience('FINN', testFormData1)

        newSummerExperiences = list(CCEMinorProposal.select().where(CCEMinorProposal.student == "FINN", CCEMinorProposal.proposalType == 'Summer Experience'))
        assert len(newSummerExperiences) == 1

        # create the summer experience with the test data and verify FINN has a new entry
        with app.app_context():
            g.current_user = "glek"
            createSummerExperience("FINN", testFormData2)

        newSummerExperiences = list(CCEMinorProposal.select().where(CCEMinorProposal.student == "FINN", CCEMinorProposal.proposalType == 'Summer Experience'))
        assert len(newSummerExperiences) == 2

        transaction.rollback()

@pytest.mark.integration
def test_createOtherEngagementRequest():
    with mainDB.atomic() as transaction:
        User.create(username="FINN",
                    firstName="Not",
                    lastName="Yet",
                    email="FINN@berea.edu",
                    bnumber="B91111111")
        
        User.create(username="glek",
                    firstName="kafui",
                    lastName="gle",
                    email="kaf@berea.edu",
                    bnumber="B91111113")
        
        testInfo = {'term': 4,
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
                    'filename': 'test_file.txt',
                   }

        # Save the requested event to the database
        with app.app_context():
            g.current_user = "glek"
            createOtherEngagementRequest('FINN', testInfo)

        # Get the actual saved request from the database (the most recent one)
        initialOtherExperiences = CCEMinorProposal.select().where(CCEMinorProposal.proposalType== 'Other Engagement', CCEMinorProposal.student == "FINN")
       
        assert len(initialOtherExperiences) == 1 

        transaction.rollback()



@pytest.mark.integration
def test_removeProposal():
    '''creates a test course with all foreign key fields. tests if they can
    be deleted'''

    testProposalId = 999

    with mainDB.atomic() as transaction:

        assert list(CCEMinorProposal.select(CCEMinorProposal.id).where(CCEMinorProposal.id == testProposalId)) == []
            

        User.create(username="glek",
                    firstName="Not",
                    lastName="Yet",
                    email="glek@berea.edu",
                    bnumber="B91111111")


        testInfo = {'term': 3,
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
                   }


        testProposal = CCEMinorProposal.create(id=testProposalId,
                                student = 'glek',
                                proposalType = 'Other Engagement',
                                createdBy = "ramsayb2",
                                status = 'Pending',
                                **testInfo
                            )
        assert list(CCEMinorProposal.select().where(CCEMinorProposal.id == testProposalId)) == [testProposal]
        
        with app.app_context():
            print('####')
            g.current_user = "glek"
            removeProposal(testProposalId)

        assert list(CCEMinorProposal.select().where(CCEMinorProposal.id == testProposalId)) == []

        transaction.rollback()



# creates base object for events tests
proposalFileStorageObject = [FileStorage(filename= "proposal.pdf")]

handledEventFile = FileHandler(proposalFileStorageObject, proposalId=999)

handledEventFileRecurring = FileHandler(proposalFileStorageObject, proposalId=999)
@pytest.mark.integration
def test_saveFiles():
    with mainDB.atomic() as transaction:
        # test event
        handledEventFile.saveFiles(saveOriginalFile = AttachmentUpload.get_by_id(999))
        
        assert AttachmentUpload.select().where(AttachmentUpload.fileName == '999/proposalId.pdf').exists()
        
        # test saving 2nd event in a hypothetical recurring series
        handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
        assert AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').exists()
        assert 1 == AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').count()
        
        handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
        assert 1 == AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').count()

        # test course
        handledCourseFile.saveFiles()
        assert AttachmentUpload.select().where(AttachmentUpload.fileName == 'coursefile.pdf').exists()

        # removes saved paths from file directory
        os.remove(handledEventFile.getFileFullPath('15/eventfile.pdf'))
        os.remove(handledCourseFile.getFileFullPath('coursefile.pdf'))
        
        transaction.rollback()

@pytest.mark.integration
def test_deleteFile():
    with mainDB.atomic() as transaction:
        # creates file in event file directory for deletion
        handledEventFile.saveFiles(saveOriginalFile = Event.get_by_id(15))

        # creates a second file to simulate recurring events
        handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
        
        # creates a course file for deletion
        handledCourseFile.saveFiles()

        # delete events
        path = handledEventFile.getFileFullPath("15/eventfile.pdf")

        # if multiple event attachments reference the same path, the path is only removed after the final referencing instance has been deleted.
        firstevent = AttachmentUpload.get(AttachmentUpload.event == 15)
        handledEventFile.deleteFile(firstevent.id)
        assert os.path.exists(path)==True
    
        secondevent = AttachmentUpload.get(AttachmentUpload.event == 16)
        handledEventFile.deleteFile(secondevent.id)
        assert os.path.exists(path)==False

        # delete courses
        coursefile = AttachmentUpload.get(AttachmentUpload.course == 1)
        
        path = handledCourseFile.getFileFullPath('coursefile.pdf')

        handledCourseFile.deleteFile(coursefile.id)
        
        assert os.path.exists(path)==False


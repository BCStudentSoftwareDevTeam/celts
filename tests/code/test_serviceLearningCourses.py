import pytest
from flask import g
from werkzeug.datastructures import MultiDict

from app import app
from app.models import mainDB
from app.models.user import User
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.logic.serviceLearningCourses import *

@pytest.mark.integration
def test_getServiceLearningCoursesData():
    '''tests for the successful implementation of populating the proposal table'''
    courseDict = getServiceLearningCoursesData('ramsayb2')
    assert 2 in courseDict
    assert 'Brian Ramsay' in courseDict[2]['faculty']
    assert ['Brian Ramsay', 'Zach Neill'] == courseDict[2]['faculty']
    assert "Submitted" == courseDict[2]['status']
    assert 'Spring 2021' in courseDict[2]['term'].description
    assert "Scott Heggen"  == courseDict[2]['creator']

    courseDict = getServiceLearningCoursesData('heggens')
    assert 3 in courseDict
    assert 'Scott Heggen' in courseDict[3]['faculty']
    assert not ['Brian Ramsay', 'Zach Neill'] == courseDict[3]['faculty']
    assert "Approved" == courseDict[3]['status']
    assert 'Summer 2021' in courseDict[3]['term'].description
    assert "Brian Ramsay"  == courseDict[3]['creator']

    courseDict = getServiceLearningCoursesData('heggens')
    assert 4 in courseDict
    assert 'Scott Heggen' not in courseDict[4]['faculty']
    assert ['Brian Ramsay', 'Ala Qasem'] == courseDict[4]['faculty']
    assert "In Progress" == courseDict[4]['status']
    assert 'Spring 2021' in courseDict[4]['term'].description
    assert "Scott Heggen"  == courseDict[4]['creator']

@pytest.mark.integration
def test_getInstructorCourses():
    """
    This test is to get the faculty intructors and check their previous courses they taught
    """
    courseDict = getInstructorCourses()
    currentFaculty = User.get_by_id("ramsayb2")
    currentFacultyCourses = courseDict[currentFaculty]
    assert 'Spanish Help' in currentFacultyCourses
    assert 'Databases' in currentFacultyCourses
    assert 'Math' not in currentFacultyCourses

@pytest.mark.integration
def test_courseManagement():
    with mainDB.atomic() as transaction:
        approvedCourse = Course.create(courseName = "Testing Approved",
                                        term = 3,
                                        status = CourseStatus.APPROVED,
                                        courseCredit = "7",
                                        createdBy = "ramsayb2",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        submittedCourse = Course.create(courseName = "Testing Submitted",
                                        term = 3,
                                        status = CourseStatus.SUBMITTED,
                                        courseCredit = "12",
                                        createdBy = "heggens",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        incompleteCourse = Course.create(courseName = "Testing Incomplete",
                                        term = 3,
                                        status = CourseStatus.IN_PROGRESS,
                                        courseCredit = "12",
                                        createdBy = "heggens",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        CourseInstructor.create(course = submittedCourse.id,
                                                    user = 'ramsayb2')
        CourseInstructor.create(course = submittedCourse.id,
                                                    user = 'neillz')
        CourseInstructor.create(course = approvedCourse.id,
                                                    user = 'ramsayb2')

        termId = 3

        unapprovedList = list(unapprovedCourses(termId))
        courseindex = unapprovedList.index(submittedCourse)

        assert approvedCourse in approvedCourses(termId)
        assert submittedCourse in unapprovedCourses(termId)
        assert incompleteCourse in unapprovedCourses(termId), "unapprovedCourses doesn't include INCOMPLETE proposals"
        assert unapprovedList[courseindex].instructors == " Brian Ramsay, Zach Neill"


        transaction.rollback()
@pytest.mark.integration
def test_withdrawProposal():
    '''creates a test course with all foreign key fields. tests if they can
    be deleted'''

    with mainDB.atomic() as transaction:

        if 99 in Course.select(Course.id):
            withdrawProposal(99)
        course = Course.create(
                id= 99,
                courseName= "Test",
                term=2,
                status= 1,
                courseCredit= "",
                createdBy= "ramsayb2",
                isAllSectionsServiceLearning= True,
                isPermanentlyDesignated= False,
                )
        question = CourseQuestion.create(
            id = 99,
            course=99,
            questionContent="Why must I create so much for just one test?",
            questionNumber=1
        )
        note = Note.create(
            id = 99,
            createdBy = "neillz",
            createdOn = "2021-10-12 00:00:00",
            noteContent = "This is a test note.",
            isPrivate = False,
            noteType = "question"
        )
        qnote = QuestionNote.create(
        id = 99,
        question = 99,
        note = 99
        )
        instructor = CourseInstructor.create(
            id= 99,
            course= 99,
            user= "ramsayb2"
        )
        participant = CourseParticipant.create(
            course= 99,
            user= "neillz",
            hoursEarned= 2.0
        )

        with app.test_request_context():
            g.current_user = "ramsayb2"
            withdrawProposal(99)

        with pytest.raises(DoesNotExist):
            Course.get_by_id(99)

        transaction.rollback()

@pytest.mark.integration
def test_renewProposal():
    with mainDB.atomic() as transaction:
        # create sample data
        course = Course.create(
                id=100,
                courseName= "Test 2",
                term=2,
                status= 1,
                courseCredit= "",
                createdBy= "heggens",
                isAllSectionsServiceLearning= True,
                isPermanentlyDesignated= False)
        question = CourseQuestion.create(
            id = 100,
            course=100,
            questionContent="Why must I create so much for just one test?",
            questionNumber=1)
        instructor = CourseInstructor.create(
            id= 100,
            course= 100,
            user= "ramsayb2"
        )

        renewProposal(course.id, 4)

        # test and make sure a new course with a different id was created
        duplicateCourse = list(Course.select().where(Course.courseName==course.courseName,
                                Course.courseCredit==course.courseCredit,
                                Course.createdBy==course.createdBy,
                                Course.isAllSectionsServiceLearning==course.isAllSectionsServiceLearning,
                                Course.isPermanentlyDesignated==course.isPermanentlyDesignated))
        assert len(duplicateCourse) == 2
        assert duplicateCourse[1].id != 100
        assert duplicateCourse[1].term == Term.get_by_id(4)
        # test and make sure a new question with a different course was created
        duplicateQuestion = list(CourseQuestion.select()
                              .join(Course)
                              .where(CourseQuestion.questionContent==question.questionContent,
                              CourseQuestion.questionNumber==question.questionNumber,
                              Course.courseName==course.courseName))
        assert len(duplicateQuestion) == 2
        assert duplicateQuestion[1].course != 100
        # test and make sure a new instructor with a different course was created
        duplicateInstructor = list(CourseInstructor.select()
                              .join(Course)
                              .where(CourseInstructor.user==instructor.user,
                              Course.courseName==course.courseName))
        assert len(duplicateInstructor) == 2
        assert duplicateInstructor[1].course != 100
        transaction.rollback()

@pytest.mark.integration
def test_update_course():
    with mainDB.atomic() as transaction:
        testUser = User.create( username="testuser",
                                bnumber="B00000001",
                                email="test@test.edu",
                                phoneNumber="555-555-5555",
                                firstName="Test",
                                lastName="User",
                                isFaculty="1")
        testingCourse = Course.create(
                                        courseName = "Testing Course",
                                        courseAbbreviation = "TC",
                                        courseCredit = 1.5,
                                        isRegularlyOccurring = 0,
                                        term = 3,
                                        status = CourseStatus.SUBMITTED,
                                        createdBy = testUser,
                                        isAllSectionsServiceLearning = 0,
                                        serviceLearningDesignatedSections = "All",
                                        sectionDesignation = "Section B",
                                        isPermanentlyDesignated = 1,
                                        isPreviouslyApproved = 1,
                                        previouslyApprovedDescription = "Hehe",
                                        hasSlcComponent = 1)

        for i in range(1, 7):
            CourseQuestion.create( course=Course.get(courseName="Testing Course"), questionNumber=i)

        testingCourseInstructor = CourseInstructor.create( course=testingCourse, user="ramsayb2")

        courseDict = MultiDict({
                        "courseName": "Changed",
                        "courseID": testingCourse,
                        "courseAbbreviation": "Chan",
                        "credit": 2,
                        "isRegularlyOccurring": 1,
                        "term": 2,
                        "slSectionsToggle": "on",
                        "slDesignation": "None",
                        "sectionDesignation":"Section A",
                        "permanentDesignation": "off",
                        "isPreviouslyApproved":0,
                        "previouslyApprovedDescription":"Hoho",
                        "hasSlcComponent": 0,
                        "1": "Question 1",
                        "2": "Question 2",
                        "3": "Question 3",
                        "4": "Question 4",
                        "5": "Question 5",
                        "6": "Question 6",
                        })
        courseDict.update(MultiDict([
                            ("instructor[]",testUser.username),
                            ("instructor[]",testingCourseInstructor.user.username)]))

        with app.test_request_context():
            g.current_user = "ramsayb2"
            updateCourse(courseDict)

        updatedCourse = Course.get_by_id(testingCourse.id)
        assert updatedCourse.courseName == "Changed"
        assert updatedCourse.courseAbbreviation == "Chan"
        assert updatedCourse.courseCredit == 2
        assert updatedCourse.isRegularlyOccurring == 1
        assert updatedCourse.status.id == CourseStatus.SUBMITTED
        assert updatedCourse.isAllSectionsServiceLearning == 1
        assert updatedCourse.sectionDesignation == "Section A"
        assert updatedCourse.serviceLearningDesignatedSections == "None"
        assert not updatedCourse.isPermanentlyDesignated
        assert updatedCourse.isPreviouslyApproved == 0
        assert updatedCourse.previouslyApprovedDescription == "Hoho"
        assert updatedCourse.hasSlcComponent == 0

        for i in range(1,7):
            assert CourseQuestion.get(questionNumber=str(i), course=testingCourse.id).questionContent == courseDict[str(i)]


        instructorCount = CourseInstructor.select().where(CourseInstructor.course == updatedCourse.id).count()
        assert instructorCount == 2

        transaction.rollback()

@pytest.mark.integration
def test_pushDataToDatabase():
    
    with mainDB.atomic() as transaction:
        cpPreview = {'Fall 2019' : {'courses': {'CSC 226' : {'students': [
                        {"user":"ayisie","displayMsg":"Ebenezer Ayisi","errorMsg":""},
                        {"user":"bledsoef","displayMsg":"Finn Bledsoe","errorMsg":""}
                        ]}}},
                     'Spring 2020' : {'courses': {'HIS 236' : { 'students':[
                         {"user":"bryanta","displayMsg":"Alex Bryant","errorMsg":""}]}}},
                     'Summer 2021' : {'courses': {'CSC 450' : { 'students':[
                         {"user":"partont","displayMsg":"Tyler Parton","errorMsg":""}]}}},
                     }

        assert Term.get_or_none(Term.description =="Fall 2019") == None
        assert Term.get_or_none(Term.description == "Spring 2020") == None
        assert Term.get_or_none(Term.description == 'Summer 2021') != None

        assert Course.get_or_none(Course.courseAbbreviation == "CSC 226") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "HIS 236") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "CSC 450") == None 

        assert len(list(CourseParticipant.select())) == 5

        with app.app_context():
            g.current_user="ramsayb2" 
            saveCourseParticipantsToDatabase(cpPreview)

        assert len(list(CourseParticipant.select())) == 9

        getTestCourseParticipant = CourseParticipant.get_or_none(user_id = 'ayisie')
        getTestTerm = Term.get_or_none(description = 'Fall 2019')
        getTestCourse = Course.get_or_none(id = getTestCourseParticipant.course_id)
        assert getTestCourse.courseAbbreviation == 'CSC 226'
        assert getTestCourse.term_id == getTestTerm.id

        getTestCourseParticipant = CourseParticipant.get_or_none(user_id = 'bledsoef')
        getTestTerm = Term.get_or_none(description = 'Fall 2019')
        getTestCourse = Course.get_or_none(id = getTestCourseParticipant.course_id)
        assert getTestCourse.courseAbbreviation == 'CSC 226'
        assert getTestCourse.term_id == getTestTerm.id

        getTestCourseParticipant = CourseParticipant.get_or_none(user_id = 'bryanta')
        getTestTerm = Term.get_or_none(description = 'Spring 2020')
        getTestCourse = Course.get_or_none(id = getTestCourseParticipant.course_id)
        assert getTestCourse.courseAbbreviation == 'HIS 236'
        assert getTestCourse.term_id == getTestTerm.id

        getTestCourseParticipant = CourseParticipant.get_or_none(user_id = 'partont')
        getTestTerm = Term.get_or_none(description = 'Summer 2021')
        getTestCourse = Course.get_or_none(id = getTestCourseParticipant.course_id)
        assert getTestCourse.courseAbbreviation == 'CSC 450'
        assert getTestCourse.term_id == getTestTerm.id


        transaction.rollback()

@pytest.mark.integration
def test_parseUpload():
    valid_file_path = 'tests/files/parseUpload_ValidTest.xlsx'  
    result = parseUploadedFile(valid_file_path)
    assert isinstance(result, tuple)
    assert len(result) == 2
    parsedParticipants, errors = result

    assert len(errors) == 0
    assert "Fall 2020" in parsedParticipants
    assert parsedParticipants["Fall 2020"] == {
        "displayMsg":"Fall 2020",
        "errorMsg":"",
        "courses": {
            "CSC 226": {
                "displayMsg": "CSC 226 will be created.",
                "errorMsg": "",
                "students": [
                    {"user":"agliullovak","displayMsg":"Karina Agliullova","errorMsg":""},
                    {"user":"ayisie","displayMsg":"Ebenezer Ayisi","errorMsg":""}
                    ]
            },
            'FRN 103': {
                "displayMsg": "FRN 103 matched to the existing course Frenchy Help.",
                "errorMsg": "",
                "students":[{"user":"bryanta","displayMsg":"Alex Bryant","errorMsg":""}]
            }
        }
    }

    invalid_file_path = 'tests/files/parseUpload_InvalidTest.xlsx'  
    result = parseUploadedFile(invalid_file_path)
    assert isinstance(result, tuple)
    assert len(result) == 2
    result, errors = result

    # all the errors are there
    assert len(errors) == 2
    # but some errors are general
    assert len([e for e in errors if e[1] == 1]) == 1
    assert len(result) == 4

import pytest

from flask import g
from peewee import DoesNotExist

from app import app
from app.models import mainDB
from app.models.term import Term
from app.models.user import User
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.note import Note

from app.logic.serviceLearningCoursesData import withdrawProposal, renewProposal, getServiceLearningCoursesData
from app.logic.manageSLFaculty import getInstructorCourses
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

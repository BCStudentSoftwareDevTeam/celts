import pytest

from flask import Flask, g
from datetime import datetime
from peewee import DoesNotExist

from app.models.user import User
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.note import Note

from app.logic.serviceLearningCoursesData import withdrawProposal, getServiceLearningCoursesData
from app.logic.manageSLFaculty import getCourseDict
@pytest.mark.integration
def test_getServiceLearningCoursesData():
    '''tests for the successful implementation of populating the proposal table'''
    courseDict = getServiceLearningCoursesData('ramsayb2')
    assert 'Spanish Help' in courseDict
    assert 'Brian Ramsay' in courseDict['Spanish Help']['faculty']
    assert ['Brian Ramsay', 'Zach Neill'] == courseDict['Spanish Help']['faculty']
    assert 'Approved' in courseDict['Spanish Help']['status']
    assert 'Spring A 2021' in courseDict['Spanish Help']['term'].description
    assert not 'Internship' in courseDict

@pytest.mark.integration
def test_withdrawProposal():
    '''creates a test course with all foreign key fields. tests if they can
    be deleted'''
    if 99 in Course.select(Course.id):
        withdrawProposal(99)
    course = Course.create(
            id= 99,
            courseName= "Test",
            term=2,
            status= 1,
            courseCredit= "",
            createdBy= "",
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
        isPrivate = False
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

    withdrawProposal(99)
    with pytest.raises(DoesNotExist):
        Course.get_by_id(99)

@pytest.mark.integration
def test_getCourseDict():
    """
    This test is to get the faculty intructors and check their previous courses they taught
    """
    courseDict = getCourseDict()
    currentFaculty = User.get_by_id("ramsayb2")
    currentFacultyCourses = courseDict[currentFaculty]
    assert 'Spanish Help' in currentFacultyCourses
    assert 'Databases' in currentFacultyCourses
    assert 'Math' not in currentFacultyCourses

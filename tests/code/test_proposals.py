import pytest
from flask import Flask, g
from peewee import DoesNotExist
from app.models.program import Program
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.user import User
from app.logic.courseProposals import deleteProposal, getProposalData, authorized

@pytest.mark.integration
def test_isCorrectData():
    '''tests for the successful implementation of populating the proposal table'''
    courseDict = getProposalData('ramsayb2')
    assert 'Databases' in courseDict
    assert 'Brian Ramsay' in courseDict['Databases']['faculty']
    assert ['Brian Ramsay', 'Zach Neill'] == courseDict['Spanish Help']['faculty']
    assert 'Approved' in courseDict['Spanish Help']['status']
    assert 'Spring A 2021' in courseDict['Spanish Help']['term'].description
    assert not 'Internship' in courseDict

@pytest.mark.integration
def test_deletesProposal():
    '''creates a test course with all foreign key fields. tests if they can
    be deleted'''
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
        course=99,
        questionContent="Why must I create so much for just one test?",
        questionNumber=1
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
    deleteProposal(99)
    with pytest.raises(DoesNotExist):
        Course.get_by_id(99)

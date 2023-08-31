import pytest 
from flask import g 
from app import app
from app.models import mainDB
from app.models.term import Term 
from app.models.course import Course
from app.models.user import User
from app.models.courseParticipant import CourseParticipant
from app.logic.serviceLearningCoursesData import parseUploadedFile, saveCourseParticipantsToDatabase

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

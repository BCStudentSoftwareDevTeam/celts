import pytest 
from flask import g 
from app import app
from app.models import mainDB
from app.models.term import Term 
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.logic.serviceLearningCoursesData import parseUploadedFile, saveCourseParticipantsToDatabase

@pytest.mark.integration
def test_pushDataToDatabase():
    
    with mainDB.atomic() as transaction:
        courseParticipantPreview = {'Fall 2019' : {'CSC 226' : [['Ebenezer Ayisi', 'B00739736'], ['Finn Bledsoe', 'B00776544']]},
                                    'Spring 2020' : {'HIS 236' : [['Alex Bryant', 'B00708826']]},
                                    'Summer 2021' : {'CSC 450' : [['Tyler Parton', 'B00751360']]}}

        assert Term.get_or_none(Term.description =="Fall 2019") == None
        assert Term.get_or_none(Term.description == "Spring 2020") == None
        assert Term.get_or_none(Term.description == 'Summer 2021') != None

        assert Course.get_or_none(Course.courseAbbreviation == "CSC 226") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "HIS 236") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "CSC 450") == None 

        assert len(list(CourseParticipant.select())) == 5

        with app.app_context():
            g.current_user="ramsayb2" 
            saveCourseParticipantsToDatabase(courseParticipantPreview)

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
    assert len(result) == 3
    errorFlag, courseParticipantPreview, errorList = result

    assert not errorFlag
    assert not errorList
    assert isinstance(courseParticipantPreview, dict)
    assert len(courseParticipantPreview) == 4

    invalid_file_path = 'tests/files/parseUpload_InvalidTest.xlsx'  
    result = parseUploadedFile(invalid_file_path)
    assert isinstance(result, tuple)
    assert len(result) == 3
    errorFlag, courseParticipantPreview, errorList = result

    assert errorFlag
    assert errorList
    assert isinstance(courseParticipantPreview, dict)
    assert len(courseParticipantPreview) == 4




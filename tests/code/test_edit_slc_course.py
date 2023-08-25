import pytest
from flask import g
from werkzeug.datastructures import MultiDict

from app import app
from app.models import mainDB
from app.models.course import Course
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.user import User
from app.models.courseStatus import CourseStatus
from app.logic.courseManagement import updateCourse

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

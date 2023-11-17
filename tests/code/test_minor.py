from app.logic.minor import *
from peewee import *
from app.models.course import Course
from app.models.courseInstructor import CourseInstructor
from app.models import mainDB
import pytest

@pytest.mark.integration
def test_getCourseInformation():
    with mainDB.atomic() as transaction:
        testCourse = Course.create(courseName="test get course information",
                      courseAbbreviation="TGCI",
                      sectionDesignation="something",
                      courseCredit=1.0,
                      term=3,
                      status=1,
                      createdBy="bledsoef")
        
        testCourseInstructor = CourseInstructor.create(course=testCourse.id, user="bledsoef")
        
        courseInformation = getCourseInformation(testCourse.id)

        testCourseDict = model_to_dict(testCourse)

        manualCourseInformation = {"instructors":[testCourseInstructor.user.firstName + " " + testCourseInstructor.user.lastName], "course": testCourseDict}
        print(manualCourseInformation)
        print(courseInformation)
        print(courseInformation == manualCourseInformation)
        assert manualCourseInformation == courseInformation
        transaction.rollback()


@pytest.mark.integration
def test_updateMinorInterest():
    with mainDB.atomic() as transaction:

        transaction.rollback()

@pytest.mark.integration
def test_getProgramEngagementHistory():
    with mainDB.atomic() as transaction:
        
        transaction.rollback()

@pytest.mark.integration
def test_getCommunityEngagementByTerm():
    with mainDB.atomic() as transaction:
        
        transaction.rollback()

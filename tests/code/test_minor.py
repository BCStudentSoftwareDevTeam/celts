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
def test_updateMinorInterest():
    with mainDB.atomic() as transaction:
        test_user = User.create(
            username="FINN",
            firstName="Not",
            lastName="Yet",
            email=f"FINN@berea.edu",
            bnumber="B91111111")
        
        user = User.get_by_id("FINN")
        # make sure users have the default values of false and not interested, respectively
        assert user.minorInterest == False
        assert user.minorStatus == "No interest"
        updateMinorInterest("FINN")
        
        user = User.get_by_id("FINN")
        # make sure updateMinorInterest works correctly
        assert user.minorInterest == True
        assert user.minorStatus == "Interested"
        
        # verify unchecking box will restore defaults
        updateMinorInterest("FINN")
        
        user = User.get_by_id("FINN")  
        assert user.minorInterest == False
        assert user.minorStatus == "No interest"
        transaction.rollback()

@pytest.mark.integration
def test_getProgramEngagementHistory():
    with mainDB.atomic() as transaction:
        
        transaction.rollback()

@pytest.mark.integration
def test_getCommunityEngagementByTerm():
    with mainDB.atomic() as transaction:
        
        transaction.rollback()

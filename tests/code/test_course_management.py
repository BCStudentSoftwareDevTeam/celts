import pytest

from app.models import mainDB
from app.logic.courseManagement import *
from app.models.course import Course
from app.models.courseInstructor import CourseInstructor

@pytest.mark.integration
def test_course_management():
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

import pytest

from app.models import mainDB
from app.logic.courseManagement import *
from app.models.course import Course
from app.models.courseInstructor import CourseInstructor

@pytest.mark.integration
def test_course_management():
    with mainDB.atomic() as transaction:
        testingCourse = Course.create(courseName = "Testing Approved",
                                        term = 3,
                                        status = 1,
                                        courseCredit = "7",
                                        createdBy = "Mayjue",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        testingCourse = Course.create(courseName = "Testing Pending",
                                        term = 3,
                                        status = 2,
                                        courseCredit = "12",
                                        createdBy = "Tyler Parton",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        getPendingTestId = Course.get(Course.courseName == "Testing Pending")
        getApprovedTestId = Course.get(Course.courseName == "Testing Approved")

        pendingCourseInstructor = CourseInstructor.create(course = getPendingTestId.id,
                                                    user = 'ramsayb2')
        approvedCourseInstructor = CourseInstructor.create(course = getApprovedTestId.id,
                                                    user = 'ramsayb2')

        termId = 3
        pending = pendingCourses(termId)
        approved = approveCourses(termId)
        pendingCourse = []
        approvedCourse = []
        for courses in pending:
            pendingCourse.append(courses.course.courseName)
        for courses in approved:
            approvedCourse.append(courses.course.courseName)


        assert "Testing Approved" in approvedCourse
        assert "Testing Pending" in pendingCourse

        transaction.rollback()

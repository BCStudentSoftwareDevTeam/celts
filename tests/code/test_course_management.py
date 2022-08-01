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
                                        status = CourseStatus.APPROVED,
                                        courseCredit = "7",
                                        createdBy = "ramsayb2",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        testingCourse = Course.create(courseName = "Testing Submitted",
                                        term = 3,
                                        status = CourseStatus.SUBMITTED,
                                        courseCredit = "12",
                                        createdBy = "heggens",
                                        isAllSectionsServiceLearning = 0,
                                        isPermanentlyDesignated = 0)

        getSubmittedTestId = Course.get(Course.courseName == "Testing Submitted")
        getApprovedTestId = Course.get(Course.courseName == "Testing Approved")

        submittedCourseInstructor = CourseInstructor.create(course = getSubmittedTestId.id,
                                                    user = 'ramsayb2')
        approvedCourseInstructor = CourseInstructor.create(course = getApprovedTestId.id,
                                                    user = 'ramsayb2')

        termId = 3
        submitted = submittedCourses(termId)
        approved = approvedCourses(termId)
        submittedCourse = []
        approvedCourse = []
        for courses in submitted:
            submittedCourse.append(courses.courseName)
        for courses in approved:
            approvedCourse.append(courses.courseName)


        assert "Testing Approved" in approvedCourse
        assert "Testing Submitted" in submittedCourse

        transaction.rollback()

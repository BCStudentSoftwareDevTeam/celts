from app.models.user import User
from app.models.courseInstructor import CourseInstructor
from app.models.course import Course

def getInstructorCourses():
    """
    This function selects all the Instructors Name and the previous courses
    """
    instructors = (CourseInstructor.select(CourseInstructor, User, Course)
                                   .join(User).switch()
                                   .join(Course))
    result = {}

    for instructor in instructors:
        result.setdefault(instructor.user, [])
        if instructor.course.courseName not in result[instructor.user]:
            result[instructor.user].append(instructor.course.courseName)

    return result

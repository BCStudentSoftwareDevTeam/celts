from app.models.user import User
from app.models.courseInstructor import CourseInstructor

def getCourseDict():
    """
    This function selects all the Intructors Name and the previous courses
    """
    courseInstructors = CourseInstructor.select()
    course_dict = {}

    for instructor in courseInstructors:
        course_dict.setdefault(instructor.user, [])
        if instructor.course.courseName not in course_dict[instructor.user]:
            course_dict[instructor.user].append(instructor.course.courseName)
    return course_dict

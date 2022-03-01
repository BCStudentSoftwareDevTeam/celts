from app.models.user import User
from app.models.courseInstructor import CourseInstructor

def getCourseDict():
    """
    This function selects all the Intructors Name and the previous courses
    """
    users = User.select().where(User.isFaculty)
    courseInstructors = CourseInstructor.select()
    course_dict = {}

    for i in courseInstructors:
        course_dict.setdefault(i.user, []).append(i.course.courseName)
    return course_dict

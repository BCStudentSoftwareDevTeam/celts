from app.models.user import User
from app.models.courseInstructor import CourseInstructor

def getCourseDict():
    users = User.select().where(User.isFaculty)
    courseInstructors = CourseInstructor.select()
    course_dict = {}

    for i in courseInstructors:
        course_dict.setdefault(i.user, []).append(i.course.courseName)
    return course_dict

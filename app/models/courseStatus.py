# from app.models import*
from app.models import baseModel
from peewee import CharField


# class CourseStatus(baseModel):
#     status = CharField()
#     IN_PROGRESS = 1
#     SUBMITTED = 2
#     APPROVED = 3
#     IMPORTED = 4 

class CourseStatus(baseModel):
    status = CharField()
    IN_PROGRESS = 'IN_PROGRESS'
    SUBMITTED = 'SUBMITTED'
    APPROVED = 'APPROVED'
    IMPORTED = 'IMPORTED'

# def get_course_status(course_id):
#     from app.models.course import Course  # Import inside the function to avoid circular import
#     course = Course.query.get(course_id)
#     return course.status.status_name if course and course.status else 'Unknown'


# def get_course_status(course_id):
    # from app.models.course import Course
#     course = Course.get_by_id(course_id)
#     status = course.status.status if course and course.status else 'Unknown'
#     print(f"Course ID: {course_id}, Status: {status}")  # Debug print
#     return status

def get_course_status(course_id):
    from app.models.course import Course
    course = Course.get_by_id(course_id)
    if course and course.status:
        status = course.status.status
        print(f"Course ID: {course_id}, Status: {status}")  # Debug print
        return status
    else:
        print(f"Course ID: {course_id}, Status: Unknown")  # Debug print
        return 'Unknown'
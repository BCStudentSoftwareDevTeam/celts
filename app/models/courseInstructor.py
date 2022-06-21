from app.models import*
from app.models.course import Course
from app.models.instructor import Instructor

class CourseInstructor(baseModel):
    course = ForeignKeyField(Course, backref="courseInstructors")
    instructor = ForeignKeyField(Instructor)

from app.models import*
from app.models.course import Course
from app.models.user import User

class CourseInstructor(baseModel):
    course = ForeignKeyField(Course)
    user = ForeignKeyField(User)

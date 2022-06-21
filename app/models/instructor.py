from app.models import*
from app.models.user import User
from app.models.course import Course


class Instructor(baseModel):
    instructorName = ForeignKeyField(User)
    courseName = ForeignKeyField(Course)
    

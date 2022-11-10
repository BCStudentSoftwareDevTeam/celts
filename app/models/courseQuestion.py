from app.models import *
from app.models.course import Course

class CourseQuestion(baseModel):
    course = ForeignKeyField(Course)
    questionContent = TextField()
    questionNumber = IntegerField()

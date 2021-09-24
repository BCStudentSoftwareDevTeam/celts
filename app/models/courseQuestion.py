from app.models import *
from app.models.course import Course

class CourseQuestion(baseModel):
    questionContents = CharField()
    courseID = ForeignKeyField(Course)

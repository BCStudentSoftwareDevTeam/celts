from app.models import *
from app.models.courseQuestion import CourseQuestion
from app.models.note import Note

class QuestionNote(baseModel):
    question = ForeignKeyField(CourseQuestion)
    note = ForeignKeyField(Note)

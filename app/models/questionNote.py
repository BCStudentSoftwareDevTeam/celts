from app.models import *
from app.models.courseQuestion import CourseQuestion
from app.models.note import Note
class QuestionNote(baseModel):
    questionID = ForeignKeyField(CourseQuestion)
    note_id = ForeignKeyField(Note)

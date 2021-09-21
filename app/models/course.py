from app.models import *
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.note import Note

class Course(baseModel):
    courseName = CharField()
    term = ForeignKeyField(Term)
    status = ForeignKeyField(CourseStatus)
    courseCredit = CharField()
    createdBy = CharField()
    isAllSectionsServiceLearning = BooleanField(default=False)
    isPermanentlyDesignated = BooleanField(default=False)
    sectionBQuestion1 = CharField()
    sectionBQuestion2 = CharField()
    sectionBQuestion3 = CharField()
    sectionBQuestion4 = CharField()
    sectionBQuestion5 = CharField()
    sectionBQuestion6 = CharField()
    sectionBQuestion1Note = ForeignKeyField(Note)
    # sectionBQuestion2Note = ForeignKeyField(Note)
    # sectionBQuestion3Note = ForeignKeyField(Note)
    # sectionBQuestion4Note = ForeignKeyField(Note)
    # sectionBQuestion5Note = ForeignKeyField(Note)
    # sectionBQuestion6Note = ForeignKeyField(Note)

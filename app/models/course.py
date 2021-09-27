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

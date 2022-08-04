from app.models import *
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.note import Note
from app.models.user import User

class Course(baseModel):
    courseName = CharField()
    courseAbbreviation = CharField()
    courseCredit = FloatField()
    courseOccurrence = CharField()
    term = ForeignKeyField(Term, null = True)
    status = ForeignKeyField(CourseStatus)
    createdBy = ForeignKeyField(User)
    isAllSectionsServiceLearning = BooleanField(default=False)
    serviceLearningDesignatedSections = CharField()
    isPermanentlyDesignated = BooleanField(default=False)

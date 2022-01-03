from app.models import *
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.note import Note

class Course(baseModel):
    courseName = CharField()
    courseAbbreviation = CharField()
    courseCredit = FloatField()
    isRegularlyOccuring = BooleanField(default=False)
    term = ForeignKeyField(Term)
    status = ForeignKeyField(CourseStatus)
    createdBy = CharField()
    isAllSectionsServiceLearning = BooleanField(default=False)
    serviceLearningDesignatedSections = CharField()
    isPermanentlyDesignated = BooleanField(default=False)

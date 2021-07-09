from app.models import *
from app.models.term import Term
from app.models.courseStatus import CourseStatus

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

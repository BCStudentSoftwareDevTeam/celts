from app.models import *
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.note import Note
from app.models.user import User

class Course(baseModel):
    courseName = CharField()
    courseAbbreviation = CharField()
    sectionDesignation = CharField()
    courseCredit = FloatField()
    term = ForeignKeyField(Term, null = True)
    status = ForeignKeyField(CourseStatus)
    createdBy = ForeignKeyField(User)
    serviceLearningDesignatedSections = TextField()
    previouslyApprovedDescription = TextField()
    isPermanentlyDesignated = BooleanField(default=False)
    isAllSectionsServiceLearning = BooleanField(default=False)
    isRegularlyOccurring = BooleanField(default=False)
    isPreviouslyApproved = BooleanField(default=False)
    hasSlcComponent = BooleanField(default=False)


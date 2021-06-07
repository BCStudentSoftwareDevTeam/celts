from app.models import*
from app.models.term import Term
from app.models.status import CourseStatus

class Course(baseModel):
    courseName = PrimaryKeyField(null=False)
    term = ForeignKeyField(Term, null=False)
    status = ForeignKeyField(CourseStatus, null=False)
    courseCredit = CharField(null=False)
    createdBy = CharField(null=False)
    isAllSectionsServiceLearning = BooleanField(null=True)
    isPermanentlyDesignated = BooleanField(null=True)
    sectionBQuestion1 = CharField(null=False)
    sectionBQuestion2 = CharField(null=False)
    sectionBQuestion3 = CharField(null=False)
    sectionBQuestion4 = CharField(null=False)
    sectionBQuestion5 = CharField(null=False)
    sectionBQuestion6 = CharField(null=False)

from app.models import*
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.partner import Partner

class Program(baseModel):
    programName = CharField()
    partner = ForeignKeyField(Partner, null=True)
    term = ForeignKeyField(Term)

from app.models import*
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.partner import Partner
from app.models.programCategory import ProgramCategory

class Program(baseModel):
    programName = CharField()
    partner = ForeignKeyField(Partner, null=True)
    programCategory = ForeignKeyField(ProgramCategory)

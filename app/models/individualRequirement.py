from app.models import*
from app.models.program import Program
from app.models.user import User
from app.models.term import Term
from app.models.course import Course
from app.models.certificationRequirement import CertificationRequirement


class IndividualRequirement(baseModel):
    program = ForeignKeyField(Program)
    course = ForeignKeyField(Course)
    username = CharField(primary_key = True)
    term = ForeignKeyField(Term, null = True)
    requirement = ForeignKeyField(CertificationRequirement)
    addedBy = ForeignKeyField(User)
    addedOn = DateTimeField()



from app.models import*
from app.models.term import Term
from app.models.program import Program

class Event(baseModel):
    eventID = PrimaryKeyField()
    eventName = CharField(null=False)
    term = ForeignKeyField(Term, null=False)
    timeStart = CharField(null=False)
    timeEnd = CharField(null=False)
    location = CharField(null=False)
    program = ForeignKeyField(Program, null=False)
    isRsvpRequired = BooleanField(null=False)
    isService = BooleanField(null=False)
    isRequiredForProgram = BooleanField(null=False)
    description = CharField(null=False)
    startDate = DateField(null=True)
    endDate = DateField(null=True)
    files = CharField(null=True)

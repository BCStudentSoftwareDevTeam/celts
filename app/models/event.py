from app.models import*
from app.models.term import Term
from app.models.program import Program

class Event(baseModel):
    eventName = CharField()
    term = ForeignKeyField(Term)
    description = CharField()
    timeStart = CharField()
    timeEnd = CharField()
    location = CharField()
    program = ForeignKeyField(Program)
    isRsvpRequired = BooleanField(default=False)
    isService = BooleanField(default=False)
    isRequiredForProgram = BooleanField(default=False)
    startDate = DateField(null=True)
    endDate = DateField(null=True)
    files = CharField(null=True)

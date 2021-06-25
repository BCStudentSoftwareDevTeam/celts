from app.models import*
from app.models.term import Term
from app.models.program import Program

class Event(baseModel):
    eventName = CharField()
    program = ForeignKeyField(Program, backref="events")
    term = ForeignKeyField(Term)
    description = CharField()
    timeStart = TimeField()
    timeEnd = TimeField()
    location = CharField()
    isRequiredForProgram = BooleanField(default=False)
    isRsvpRequired = BooleanField(default=False)
    isService = BooleanField(default=False)
    startDate = DateField(null=True)
    endDate = DateField(null=True)
    files = CharField(null=True)

    def __str__(self):
        return f"{self.id}: {self.description}"

from app.models import*
from app.models.term import Term
from app.models.program import Program
from datetime import datetime

class Event(baseModel):
    name = CharField()
    term = ForeignKeyField(Term)
    description = CharField()
    timeStart = TimeField()
    timeEnd = TimeField()
    location = CharField()
    isTraining = BooleanField(default=False)
    isRsvpRequired = BooleanField(default=False)
    isService = BooleanField(default=False)
    isAllVolunteerTraining = BooleanField(default=False)
    startDate = DateField()
    endDate = DateField(null=True)
    recurringId = IntegerField(null=True)
    contactEmail = CharField(null=True)
    contactName = CharField(null=True)


    _spCache = "Empty"

    def __str__(self):
        return f"{self.id}: {self.description}"

    @property
    def noProgram(self):
        return not self.programEvents.exists()

    @property
    def singleProgram(self):
        from app.models.programEvent import ProgramEvent
        if self._spCache is "Empty":
            try:
                countPE = list(self.programEvents.select(ProgramEvent, Program).join(Program))
                if len(countPE) == 1:
                    self._spCache = countPE[0].program
                else:
                    self._spCache = None
            except DoesNotExist:
                self._spCache = self

        return self._spCache

    @property
    def isPast(self):
        currentTime = datetime.now()
        startDatePassed = self.startDate < currentTime.date()
        startTimePassed = self.timeStart < currentTime.time() and self.startDate == currentTime.date()
        return startDatePassed or startTimePassed

    @property
    def isRecurring(self):
        return bool(self.recurringId)

    @property
    def isFirstRecurringEvent(self):
        firstRecurringEvent = Event.select().where(Event.recurringId==self.recurringId).order_by(Event.startDate).get()
        return firstRecurringEvent.id == self.id

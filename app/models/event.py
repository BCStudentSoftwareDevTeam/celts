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
    startDate = DateField()
    endDate = DateField(null=True)
    recurringId = IntegerField(null=True)

    def __str__(self):
        return f"{self.id}: {self.description}"

    @property
    def noProgram(self):
        return not self.programEvents.exists()

    @property
    def singleProgram(self):
        if self.programEvents.count() == 1:
            return self.programEvents.get().program
        else:
            return None
    @property
    def isPast(self):
        currentTime = datetime.now()
        startDatePassed = self.startDate < currentTime.date()
        startTimePassed = self.timeStart < currentTime.time() and self.startDate == currentTime.date()
        return startDatePassed or startTimePassed

    @property
    def isRecurring(self):
        return bool(self.recurringid)

    @property
    def isFirstRecurringEvent(self):
        firstRecurringEvent = Event.select().where(Event.recurringid==self.recurringid).order_by(Event.startDate).get()
        return firstRecurringEvent.id == self.id
    

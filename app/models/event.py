from app.models import *
from app.models.term import Term
from app.models.program import Program
from datetime import datetime

class Event(baseModel):
    name = CharField()
    term = ForeignKeyField(Term)
    description = TextField()
    timeStart = TimeField()
    timeEnd = TimeField()
    location = CharField()
    isFoodProvided = BooleanField(default=False)
    isTraining = BooleanField(default=False)
    isRsvpRequired = BooleanField(default=False)
    isService = BooleanField(default=False)
    isAllVolunteerTraining = BooleanField(default=False)
    rsvpLimit = IntegerField(null=True)
    startDate = DateField()
    endDate = DateField(null=True)
    recurringId = IntegerField(null=True)
    contactEmail = CharField(null=True)
    contactName = CharField(null=True)
    program = ForeignKeyField(Program)
    isCanceled = BooleanField(default=False)

    _spCache = "Empty"

    def __str__(self):
        return f"{self.id}: {self.description}"

    @property
    def noProgram(self):
        return not self.program_id

    @property
    def isPast(self):
        return datetime.now() >= datetime.combine(self.startDate, self.timeStart)

    @property
    def isRecurring(self):
        return bool(self.recurringId)

    @property
    def isFirstRecurringEvent(self):
        firstRecurringEvent = Event.select().where(Event.recurringId==self.recurringId).order_by(Event.id).get()
        return firstRecurringEvent.id == self.id

    @property
    def relativeTime(self):
        relativeTime = datetime.combine(self.startDate, self.timeStart) - datetime.now()

        secondsFromNow = relativeTime.seconds
        minutesFromNow = secondsFromNow // 60
        hoursFromNow = minutesFromNow // 60
        daysFromNow = relativeTime.days
        if self.isPast:
            return ""
        elif (daysFromNow):
            return f"{daysFromNow} day" + ("s" if daysFromNow > 1 else "")
        elif hoursFromNow:
            return f"{hoursFromNow} hour" + ("s" if hoursFromNow > 1 else "")
        elif minutesFromNow:
            return f"{minutesFromNow} minute" + ("s" if minutesFromNow > 1 else "")
        else:
            return f"happening now"
        
    

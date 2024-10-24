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
    isEngagement = BooleanField(default=False)
    isAllVolunteerTraining = BooleanField(default=False)
    rsvpLimit = IntegerField(null=True)
    startDate = DateField()
    endDate = DateField(null=True)
    recurringId = IntegerField(null=True)
    multipleOfferingId = IntegerField(null=True)
    contactEmail = CharField(null=True)
    contactName = CharField(null=True)
    program = ForeignKeyField(Program)
    isCanceled = BooleanField(default=False)
    deletionDate = DateTimeField(null=True)
    deletedBy = TextField(null=True)

    _spCache = "Empty"

    def __str__(self):
        return f"{self.id}: {self.description}"

    @property
    def isDeleted(self):
        return self.deletionDate is not None

    @property
    def noProgram(self):
        return not self.program_id

    @property
    def isPastStart(self):
        return datetime.now() >= datetime.combine(self.startDate, self.timeStart)  

    @property
    def isPastEnd(self):
        return datetime.now() >= datetime.combine(self.endDate, self.timeEnd) 

    @property
    def isRecurring(self):
        return bool(self.recurringId)

    @property
    def isFirstRecurringEvent(self):
        firstRecurringEvent = Event.select().where(Event.recurringId==self.recurringId).order_by(Event.id).get()
        return firstRecurringEvent.id == self.id

    @property
    def isMultipleOffering(self):
        return bool(self.multipleOfferingId)
    
    @property
    def relativeTime(self):
        relativeTime = datetime.combine(self.startDate, self.timeStart) - datetime.now()

        secondsFromNow = relativeTime.seconds
        minutesFromNow = secondsFromNow // 60
        hoursFromNow = minutesFromNow // 60
        daysFromNow = relativeTime.days
        if self.isPastStart:
            return ""
        elif (daysFromNow):
            return f"{daysFromNow} day" + ("s" if daysFromNow > 1 else "")
        elif hoursFromNow:
            return f"{hoursFromNow} hour" + ("s" if hoursFromNow > 1 else "")
        elif minutesFromNow:
            return f"{minutesFromNow} minute" + ("s" if minutesFromNow > 1 else "")
        else:
            return f"happening now"
        
    

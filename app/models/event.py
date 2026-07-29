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
    allowsLabor = BooleanField(default=False)             # Event has some labor students working in addition to volunteers
    isLaborOnly = BooleanField(default=False)               # Event is a labor meeting, specifically for labor students only 
    isTraining = BooleanField(default=False)                # Event is a training for a Program (required by volunteers to earn service hours in that program)
    isAllVolunteerTraining = BooleanField(default=False)    # Event is an All Volunteers Training (required to earn any service hours)
    isCeltsTraining = BooleanField(default=False)           # Event is a CELTS labor training (required by all CELTS labor students)
    isRsvpRequired = BooleanField(default=False)
    isService = BooleanField(default=False)
    isEngagement = BooleanField(default=False)
    rsvpLimit = IntegerField(null=True)
    startDate = DateField()
    seriesId = IntegerField(null=True)
    isRepeating = BooleanField(default=False)
    contactEmail = CharField(null=True)
    contactName = CharField(null=True)
    program = ForeignKeyField(Program)
    isCanceled = BooleanField(default=False)
    deletionDate = DateTimeField(null=True)
    deletedBy = TextField(null=True)
    eventFlagsMatrix = {'isAllVolunteerTraining':   {'isAllVolunteerTraining', 
                                                     'isTraining'},
                        'isCeltsTraining':          {'isCeltsTraining',
                                                     'isLaborOnly', 
                                                     'isTraining'},
                        'isLaborOnly':              {'isLaborOnly',
                                                     'isCeltsTraining',
                                                     'isTraining'},
                        'allowsLabor':              {'allowsLabor',
                                                     'isTraining', 
                                                     'isService',
                                                     'isEngagement'},
                        'isTraining':               {'isTraining',
                                                     'isAllVolunteerTraining',
                                                     'isCeltsTraining',
                                                     'isLaborOnly',
                                                     'allowsLabor'},
                        'isService':                {'isService',
                                                     'allowsLabor'},
                        'isEngagement':             {'isEngagement',
                                                     'allowsLabor'}
                        }

    _spCache = "Empty"

    def save(self, *args, **kwargs):
        """
        Overrides the default Peewee save method. 
        NOTE: This method is not called when using Model.update()
        """
        print("Saving")
        if self.checkFlags():
            return super().save(*args, **kwargs)
        else:            
            raise IntegrityError("This combination of options is not allowed")
    
    def __str__(self):
        return f"{self.id}: {self.description}"

    def checkFlags(self):
        """
        Checks the eventFlagsMatrix to ensure the user is only picking a combination of flags that are allowed.
        """
        setFlags = []
        for attribute in self._meta.fields.keys():
            if self.eventFlagsMatrix.get(attribute):
                if getattr(self, attribute):
                    setFlags.append(attribute)
        print(setFlags)
        for setFlag in setFlags:
            allowedFlags = self.eventFlagsMatrix[setFlag]
            if not all(flag in allowedFlags for flag in setFlags):
                return False

        return True


                
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
        return datetime.now() >= datetime.combine(self.startDate, self.timeEnd) 

    @property
    def isFirstRepeatingEvent(self):
        firstRepeatingEvent = Event.select().where(Event.seriesId==self.seriesId).order_by(Event.id).get()
        return firstRepeatingEvent.id == self.id
    
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
        
    

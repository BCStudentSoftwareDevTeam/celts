from app.models.program import Program
from app.models.user import User
from app.models.event import Event

# Group events by a program - 1st function
#

def groupingEvents(termID):

    groupEvents = Event.select().where(Event.term == termID).order_by(Event.program)


# events = [item for item in groupEvents.objects()]

    #check if the program are the same


    return list(groupEvents)

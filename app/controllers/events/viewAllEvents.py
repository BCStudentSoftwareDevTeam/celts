from app.models.program import Program
from app.models.user import User
from app.models.event import Event

# Group events by a program - 1st function
#

def groupingEvents(termID):

    groupEvents = Event.select(Event.description).where(Event.term == termID).order_by(Event.program)
    # pID = Event.program.id
    for i in list(groupEvents):
        print(groupEvents.program)
    return list(groupEvents)

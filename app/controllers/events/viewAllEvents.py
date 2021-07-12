from app.models.program import Program
from app.models.user import User
from app.models.event import Event

# Group events by a program - 1st function
#

def groupingEvents(termID):

    groupEvents = (Event.select().where(Event.term == termID).order_by(Event.program))
    for item in list(groupEvents.objects()):
        print(item.program)
        print(item.timeStart)
        print(item.description)
    return groupEvents

from app.models.program import Program
from app.models.user import User
from app.models.event import Event

# Group events by a program - 1st function
#

def groupingEvents(termID):

    groupEvents = Event.select(Event.description).where(Event.term == termID).group_by(Event.program)

    return list(groupEvents)

from app.models.event import Event
from app.models.program import Program
from peewee import DoesNotExist

def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return Event.select(Event).where(Event.program == program_id)
    else:
        return Event.select()

def groupingEvents(termID):

    groupEvents = (Event.select(Event.description,Event.program).where(Event.term == termID).order_by(Event.program))
    for item in list(groupEvents.objects()):
        print(item.program)
    return groupEvents

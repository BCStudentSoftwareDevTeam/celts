from app.models.event import Event
from app.models.program import Program
from peewee import DoesNotExist
from app.models.programCategory import ProgramCategory
def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return Event.select(Event).where(Event.program == program_id)
    else:
        return Event.select()

def groupingEvents(termID):

    groupEvents = (Event.select().join(Program).join(ProgramCategory).where(Event.term == termID).order_by(Event.program.programCategory,Event.program))

    return groupEvents

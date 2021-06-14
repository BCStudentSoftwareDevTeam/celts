from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from peewee import DoesNotExist

def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return Event.select(Event).join(ProgramEvent).where(ProgramEvent.program == program_id).distinct()
    else:
        return Event.select()


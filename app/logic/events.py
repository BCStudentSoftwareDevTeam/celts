from app.models.event import Event
from app.models.program import Program
from peewee import DoesNotExist

def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return Event.select().where(Event.program == program_id)
    else:
        return Event.select()


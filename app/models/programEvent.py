from app.models import *
from app.models.program import Program
from app.models.event import Event

class ProgramEvent(baseModel):
    program = ForeignKeyField(Program)
    event = ForeignKeyField(Event)

    class Meta:
        primary_key=CompositeKey('program', 'event')

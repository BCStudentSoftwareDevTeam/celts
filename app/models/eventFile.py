from app.models import*
from app.models import Event
from app.models import File

class EventFile(baseModel):
    file = ForeignKeyField(File)
    event = ForeignKeyField(Event)

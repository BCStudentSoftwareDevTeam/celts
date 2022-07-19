from app.models import*
from app.models.event import Event
from app.models.file import File

class EventFile(baseModel):
    file = ForeignKeyField(File)
    event = ForeignKeyField(Event)

@property
    def addFile(self):
        

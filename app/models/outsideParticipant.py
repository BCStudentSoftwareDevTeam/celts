from app.models import*
from app.models.event import Event
from app.models.allOutsideParticipants import AllOutsideParticipants

class OutsideParticipant(baseModel):
    participant = ForeignKeyField(AllOutsideParticipants)
    event = ForeignKeyField(Event)

    

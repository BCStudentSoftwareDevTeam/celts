from app.models import*
from app.models.user import User
from app.models.event import Event

from app.models.outsideParticipant import OutsideParticipant

class EventOutsideParticipants(baseModel):
    outsideParticipant = ForeignKeyField(OutsideParticipant)
    event = ForeignKeyField(Event)

    class Meta:
        primary_key=CompositeKey('outsideParticipant','event')

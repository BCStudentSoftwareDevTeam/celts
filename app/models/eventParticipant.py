from app.models import*
from app.models.user import User
from app.models.event import Event

class EventParticipant(baseModel):
    participantID = PrimaryKeyField()
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)
    hoursEarned = CharField(null=True)

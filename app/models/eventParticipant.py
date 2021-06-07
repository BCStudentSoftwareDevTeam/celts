from app.models import*
from app.models.user import User
from app.models.event import Event

class EventParticipant(baseModel):
    participantID = PrimaryKeyField()
    user = ForeignKeyField(User, null=False)
    event = ForeignKeyField(Event, null=False)
    hoursEarned = CharField(null=True)

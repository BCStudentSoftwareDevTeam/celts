from app.models import*
from app.models.user import User
from app.models.event import Event

class EventParticipant(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)
    rsvp = BooleanField(default=False)
    attended = BooleanField(default=False)
    hoursEarned = CharField(null=True)

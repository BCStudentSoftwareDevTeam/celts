from app.models import*
from app.models.user import User
from app.models.event import Event
from datetime import datetime
class EventParticipant(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)
    hoursEarned = FloatField(null=True)
    swipeIn = DateTimeField(default=datetime.now)
    swipeOut = DateTimeField()

from app.models import *
from app.models.user import User
from app.models.event import Event


class EventParticipant(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)
    hoursEarned = FloatField(null=True)

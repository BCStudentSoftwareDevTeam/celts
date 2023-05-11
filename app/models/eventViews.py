from app.models import*
from app.models.user import User
from app.models.event import Event
import datetime

class EventView(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)
    viewedOn = DateTimeField(default=datetime.datetime.now)

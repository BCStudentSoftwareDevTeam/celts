from app.models import* 
from app.models.user import User 
from app.models.event import Event

class EventRsvpLogs(baseModel):
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField()
    rsvpLogContent = CharField()
    event = ForeignKeyField(Event, backref="rsvpLogs")
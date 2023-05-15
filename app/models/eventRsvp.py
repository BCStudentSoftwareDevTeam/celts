from datetime import datetime
from app.models import*
from app.models.user import User
from app.models.event import Event

class EventRsvp(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event, backref="rsvps")
    rsvpTime = DateTimeField(default=datetime.now)
    rsvpWaitlist = BooleanField(default=False)


    class Meta:
        indexes = ( (('user', 'event'), True), )

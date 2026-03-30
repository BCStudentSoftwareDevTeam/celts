from datetime import datetime
from app.models import*
from app.models.user import User
from app.models.event import Event

class EventRsvp(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event, backref="rsvps")
    rsvpTime = DateTimeField(default=datetime.now)
    rsvpWaitlist = BooleanField(default=False)

    @property
    def rsvp(self):
        # EventRsvp always represents an RSVP record, including invited participants.
        return True

    class Meta:
        indexes = ( (('user', 'event'), True), )

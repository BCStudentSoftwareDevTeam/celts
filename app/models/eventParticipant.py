from app.models import*
from app.models.user import User
from app.models.event import Event

class EventParticipant(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event, backref="participants")
    hoursEarned = FloatField(null=True)

    # Add this property so that we can combine these objects with EventRsvp objects in one array
    @property
    def rsvpWaitlist(self):
        return False

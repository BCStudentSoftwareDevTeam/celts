from app.models import*
from app.models.user import User
from app.models.event import Event

class EventParticipant(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event, backref="participants")
    hoursEarned = FloatField(null = False, default = 0)
    didWork = BooleanField(null = False, default = False)
    isLabor = BooleanField(null = False, default = False) # This field is used to indicate if a user is a volunteer or a labor participant. False is volunteer, true is labor.

    # Add this property so that we can combine these objects with EventRsvp objects in one array
    @property
    def rsvpWaitlist(self):
        return False

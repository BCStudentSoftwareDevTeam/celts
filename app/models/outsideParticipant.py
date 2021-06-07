from app.models import*
from app.models.event import Event

class OutsideParticipant(baseModel):
    outsideParticipantID = PrimaryKeyField()
    event = ForeignKeyField(Event, null=False)
    firstName = CharField(null=False)
    lastName = CharField(null=False)
    email = CharField(null=False)
    phoneNumber = CharField(null=False)

from app.models import*
from app.models.event import Event

class OutsideParticipant(baseModel):
    email = CharField(primary_key=True)
    firstName = CharField()
    lastName = CharField()
    event = ForeignKeyField(Event)
    phoneNumber = CharField()

from app.models import*
from app.models.event import Event

class OutsideParticipant(baseModel):
    event = ForeignKeyField(Event)
    firstName = CharField()
    lastName = CharField()
    email = CharField()
    phoneNumber = CharField()

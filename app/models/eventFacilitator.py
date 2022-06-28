from app.models import*
from app.models.user import User
from app.models.event import Event

class EventFacilitator(baseModel):
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)

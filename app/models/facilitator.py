from app.models import*
from app.models.user import User
from app.models.event import Event

class Facilitator(baseModel):
    facilitatorID = PrimaryKeyField()
    user = ForeignKeyField(User)
    event = ForeignKeyField(Event)

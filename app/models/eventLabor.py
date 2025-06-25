from app.models import *
from app.models.user import User
from app.models.event import Event

class EventLabor(baseModel):
    user = ForeignKeyField(User, null = False)
    hoursWorked =  FloatField(null = False, default = 0)
    event = ForeignKeyField(Event, null = False)
    didWork = BooleanField(null = False, default = False)

from app.models import *
from app.models.event import Event


class EventFile(baseModel):
    event = ForeignKeyField(Event)
    fileName = CharField()

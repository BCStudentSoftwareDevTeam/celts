from app.models import*
from app.models.event import Event
from app.models.course import Course


class EventFile(baseModel):
    event = ForeignKeyField(Event, null=True)
    course = ForeignKeyField(Course, null=True)
    fileName = CharField()

from app.models import*
from app.models.event import Event
from app.models.course import Course


class AttachmentUpload(baseModel):
    event = ForeignKeyField(Event, null=True)
    course = ForeignKeyField(Course, null=True)
    isDisplayed = BooleanField(default=False)
    fileName = CharField()

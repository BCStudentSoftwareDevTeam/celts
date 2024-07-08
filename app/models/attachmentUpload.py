from app.models import*
from app.models.event import Event
from app.models.course import Course
from app.models.otherExperience import OtherExperience


class AttachmentUpload(baseModel):
    event = ForeignKeyField(Event, null=True)
    course = ForeignKeyField(Course, null=True)
    program = ForeignKeyField(Course, null=True)
    isDisplayed = BooleanField(default=False)
    fileName = CharField()


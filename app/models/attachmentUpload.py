from app.models import*
from app.models.event import Event
from app.models.course import Course
from app.models.program import Program
from app.models.cceMinorProposal import CCEMinorProposal

class AttachmentUpload(baseModel):
    event = ForeignKeyField(Event, null=True)
    course = ForeignKeyField(Course, null=True, on_delete="CASCADE")
    program = ForeignKeyField(Program, null=True)
    proposal = ForeignKeyField(CCEMinorProposal, on_delete="CASCADE")
    isDisplayed = BooleanField(default=False)
    fileName = CharField()


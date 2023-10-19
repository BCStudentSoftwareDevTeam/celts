from app.models import *
from app.models.certificationRequirement import CertificationRequirement
from app.models.event import Event
from app.models.course import Course

class RequirementMatch(baseModel):
    requirement = ForeignKeyField(CertificationRequirement)
    event = ForeignKeyField(Event, null=True)
    course = ForeignKeyField(Course, null=True)
    otherDescription = TextField(null=True)

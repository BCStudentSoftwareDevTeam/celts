from app.models import *
from app.models.certificationRequirement import CertificationRequirement
from app.models.event import Event
from app.models.course import Course
from app.models.communityEngagementRequest import CommunityEngagementRequest

class RequirementMatch(baseModel):
    requirement = ForeignKeyField(CertificationRequirement)
    event = ForeignKeyField(Event, null=True)
    course = ForeignKeyField(Course, null=True)
    engagementRequest = ForeignKeyField(CommunityEngagementRequest, null=True)

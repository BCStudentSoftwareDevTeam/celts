from app.models import *
from app.models.certification import Certification

class CertificationRequirement(baseModel):
    certification = ForeignKeyField(Certification)
    name = CharField()
    frequency = CharField()
    isRequired = BooleanField(default=True)
    order = SmallIntegerField(null=True)

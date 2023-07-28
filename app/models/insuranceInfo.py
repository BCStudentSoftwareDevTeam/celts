from app.models import *
from app.models.user import User

class InsuranceInfo(baseModel):
    user = ForeignKeyField(User, unique=True)
    insuranceType = IntegerField(default=0)
    policyHolderName = CharField(null=True)
    policyHolderRelationship = CharField(null=True)
    insuranceCompany = CharField(null=True)
    policyNumber = CharField(null=True)
    groupNumber = CharField(null=True)
    healthIssues = CharField(null=True)
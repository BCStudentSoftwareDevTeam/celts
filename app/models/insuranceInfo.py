from app.models import *
from app.models.user import User

class InsuranceInfo(baseModel):
    user = ForeignKeyField(User, unique=True)
    insuranceType = IntegerField(default=0)
    policyHolderName = CharField(default='')
    policyHolderRelationship = CharField(default='')
    insuranceCompany = CharField(default='')
    policyNumber = CharField(default='')
    groupNumber = CharField(default='')
    healthIssues = CharField(default='')
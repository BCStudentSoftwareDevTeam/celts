from app.models import *
from app.models.user import User

class EmergencyInfo(baseModel):
    user = ForeignKeyField(User)
    name = CharField(null=True)
    relationship = CharField(null=True)
    homePhone = CharField(null=True)
    workPhone = CharField(null=True)
    cellPhone = CharField(null=True)
    emailAddress = CharField(null=True)
    homeAddress = CharField(null=True)

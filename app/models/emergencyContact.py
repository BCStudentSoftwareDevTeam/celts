from app.models import *
from app.models.user import User

class EmergencyContact(baseModel):
    user = ForeignKeyField(User)
    name = CharField(default='')
    relationship = CharField(default='')
    homePhone = CharField(default='')
    workPhone = CharField(default='')
    cellPhone = CharField(default='')
    emailAddress = CharField(default='')
    homeAddress = CharField(default='')
    
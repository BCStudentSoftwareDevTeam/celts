from app.models import *
from app.models.term import Term
from app.models.user import User
import datetime

class OtherExperience(baseModel):
    student = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    hours = IntegerField()
    weeks = IntegerField()
    experienceTitle = CharField()
    experienceDescription = CharField()
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")], default='Pending')
    orgName= CharField()
    orgAddress = CharField()
    orgPhone = CharField()
    orgWebsite = CharField()
    supervisorName = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    createdOn = DateTimeField(default=datetime.datetime.now)
    createdBy = ForeignKeyField(User)

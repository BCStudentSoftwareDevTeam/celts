from app.models import *
from app.models.term import Term
from app.models.user import User
import datetime 

class CCEMinorProposal(baseModel):
    student = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    experienceName = CharField(null=True)
    experienceType = CharField(null=True)
    contentAreas = TextField(null=True)
    experienceDescription = CharField(null=True)
    roleDescription = CharField(null=True)
    orgName = CharField()
    orgAddress = CharField()
    orgPhone = CharField()
    orgWebsite = CharField()
    supervisorPhone = CharField()
    supervisorName = CharField()
    supervisorEmail = CharField()
    totalHours = IntegerField()
    weeks = IntegerField()
    hoursNotOver300 = IntegerField(null=True)
    weeksNotOver300 = IntegerField(null=True)
    description = TextField()
    filename = CharField(null=True)
    createdOn = DateTimeField(default=datetime.datetime.now)
    createdBy = ForeignKeyField(User)
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])
    isOver300Hours = BooleanField(null=True)


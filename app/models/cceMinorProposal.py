from app.models import *
from app.models.term import Term
from app.models.user import User
import datetime 

class CCEMinorProposal(baseModel):
    student = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    proposalType = CharField()
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
    totalHours = IntegerField(null=True)
    totalWeeks = IntegerField(null=True)
    description = TextField()
    filename = CharField(null=True)
    createdOn = DateTimeField(default=datetime.datetime.now)
    createdBy = ForeignKeyField(User)
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])

    @property
    def isOver300Hours(self):
        if not int(self.totalHours) or (int(self.totalHours) and int(self.totalHours) >= 300):
            return True
        return False

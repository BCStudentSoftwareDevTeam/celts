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
    createdOn = DateTimeField(default=datetime.datetime.now)
    createdBy = ForeignKeyField(User)
<<<<<<< HEAD
    status = CharField(constraints=[Check("status in ('Approved', 'In Progress', 'Submitted', 'Denied')")])
=======
    status = CharField(constraints=[Check("status in ('In Progress', 'Submitted',  'Approved', 'Denied')")])
>>>>>>> 4c3003469db964884063dd6920227859abb2a51b

    @property
    def isOver300Hours(self):
        if not int(self.totalHours) or (int(self.totalHours) and int(self.totalHours) >= 300):
            return True
        return False

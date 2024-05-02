from app.models import *
from app.models.term import Term
from app.models.user import User

class CommunityEngagementRequest(baseModel):
    user = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    experienceName = CharField()
    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    companyWebsite = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    totalHours = IntegerField()
    weeks = IntegerField()
    description = TextField()
    filename = CharField(null=True)
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])

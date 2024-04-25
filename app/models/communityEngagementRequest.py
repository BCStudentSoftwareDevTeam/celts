from app.models import *
from app.models.term import Term
from app.models.user import User

class CommunityEngagementRequest(baseModel):
    user = ForeignKeyField(User)
    experienceName = CharField()
    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    companyWebsite = CharField()
    term = ForeignKeyField(Term)
    description = TextField()
    totalHours = IntegerField()
    weeks = IntegerField()
    filename = CharField(null=True)
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])

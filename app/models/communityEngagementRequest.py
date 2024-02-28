from app.models import *
from app.models.term import Term
from app.models.user import User

class CommunityEngagementRequest(baseModel):
    user = ForeignKeyField(User)
    experienceName = CharField()
    company = CharField()
    term = ForeignKeyField(Term)
    description = TextField()
    weeklyHours = IntegerField()
    weeks = IntegerField()
    filename = CharField(null=True)
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])

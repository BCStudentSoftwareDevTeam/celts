import datetime
from app.models import *
from app.models.term import Term
from app.models.user import User

class SummerExperience(baseModel):
    user = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    roleDescription = TextField()
    experienceType = CharField()
    CceMinorContentArea = TextField()  # Store as comma-separated values or use a related table if needed
    experienceHoursOver300 = BooleanField()
    experienceHoursBelow300 = CharField(null=True)  # Optional for hours if less than 300
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")], default='Pending') # To be checked later. We might need to create a function that validates that status can only be 'Approved' if experienceType is not null.
    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    companyWebsite = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

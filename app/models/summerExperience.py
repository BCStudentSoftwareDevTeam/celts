import datetime
from app.models import *
from app.models.user import User

class SummerExperience(baseModel):
    user = ForeignKeyField(User)
    studentName = CharField()
    summerYear = CharField()
    roleDescription = TextField()
    experienceType = CharField()
    CceMinorContentArea = TextField()  # Store as comma-separated values or use a related table if needed
    experienceHoursOver300 = BooleanField()
    experienceHoursBelow300 = CharField(null=True)  # Optional for hours if less than 300
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")], default='Pending')
    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    companyWebsite = CharField()
    supervisorName = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'summerExperience'

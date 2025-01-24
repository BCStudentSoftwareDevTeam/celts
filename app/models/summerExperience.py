import datetime
from app.models import *
from app.models.user import User

class SummerExperience(baseModel):
    user = ForeignKeyField(User)
    studentName = CharField()
    summerYear = CharField()
    roleDescription = TextField()
    experienceType = CharField()
    contentAreas = TextField()  # Store as comma-separated values or use a related table if needed
    isOver300Hours = BooleanField()
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")], default='Pending')
    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    hoursNotOver300 = IntegerField(null=True)
    weeksNotOver300 = IntegerField(null=True)
    companyWebsite = CharField()
    supervisorName = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    createdOn = DateTimeField(default=datetime.datetime.now)


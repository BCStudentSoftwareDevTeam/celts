import datetime
from app.models import *
<<<<<<< HEAD
from app.models.term import Term
from app.models.user import User

class SummerExperience(baseModel):
    user = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    roleDescription = TextField()
=======
from app.models.communityEngagementRequest import CommunityEngagementRequest
from app.models.user import User
from app.logic.minor import getMinorProgress # might need it
from peewee import CharField, BooleanField, DateField, ForeignKeyField, Check
# from app.models.baseModel import BaseModel
from app.models.user import User
from app.models.communityEngagementRequest import CommunityEngagementRequest

class SummerExperience(baseModel):
    user = ForeignKeyField(User, backref='summer_experiences')
    fullName = CharField()
    bnumber = CharField()
    email = CharField()
    dateCreated = DateField()

    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    companyWebsite = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    totalHours = CharField()
    weeks = CharField()
    description = CharField()
    filename = CharField()
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])

    roleDescription = CharField()
>>>>>>> a311d3562b18384d885f5791fe67cfb8d4a59e33
    experienceType = CharField()
    CceMinorContentArea = TextField()  # Store as comma-separated values or use a related table if needed
    experienceHoursOver300 = BooleanField()
<<<<<<< HEAD
    experienceHoursBelow300 = CharField(null=True)  # Optional for hours if less than 300
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")], default='Pending') # To be checked later. We might need to create a function that validates that status can only be 'Approved' if experienceType is not null.
    company = CharField()
    companyAddress = CharField()
    companyPhone = CharField()
    companyWebsite = CharField()
    supervisorPhone = CharField()
    supervisorEmail = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
=======
    experienceHoursBelow300 = CharField()

 
>>>>>>> a311d3562b18384d885f5791fe67cfb8d4a59e33

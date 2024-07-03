from app.models import *
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
    experienceType = CharField()
    contentArea = CharField()  # Verify if the content area(s) needs to be recorded to the database as they are named or just their count
    experienceHoursOver300 = BooleanField()
    experienceHoursBelow300 = CharField()

 

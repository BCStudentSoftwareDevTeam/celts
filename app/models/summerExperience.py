from app.models import *
from app.models.communityEngagementRequest import CommunityEngagementRequest
from app.models.term import Term
from app.models.user import User
from app.logic.minor import getMinorProgress # might need it

class SummerExperience(baseModel):
    # Imported from User
    user = ForeignKeyField(User)
    fullName = User.fullName
    bnumber = User.bnumber
    email = User.email
    dateCreated = DateField()
  

    # Imported from CommunityEngagementRequest.py
    company = CommunityEngagementRequest.company
    companyAddress = CommunityEngagementRequest.companyAddress
    companyPhone = CommunityEngagementRequest.companyPhone
    companyWebsite = CommunityEngagementRequest.companyWebsite
    supervisorPhone = CommunityEngagementRequest.supervisorPhone
    supervisorEmail = CommunityEngagementRequest.supervisorEmail
    totalHours = CommunityEngagementRequest.totalHours
    weeks = CommunityEngagementRequest.weeks
    description = CommunityEngagementRequest.description
    filename = CommunityEngagementRequest.filename
    status = CommunityEngagementRequest.status

    # Added fields
    roleDescription = CharField()
    experienceType = CharField()
    contentArea = CharField()  # Verify if the content area(s) needs to be recorded to the database as they are named or just their count
    experienceHoursOver300 = BooleanField()
    experienceHoursBelow300 = CharField()
    status = CharField(constraints=[Check("status in ('Approved', 'Pending', 'Denied')")])




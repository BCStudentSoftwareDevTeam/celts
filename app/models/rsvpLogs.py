from app.models import*
from app.models.user import User

class rsvpLogs(baseModel):
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField()
    logContent =  CharField()

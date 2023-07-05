
from app.models import*
from app.models.user import User

class AdminLog(baseModel):
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField()
    logContent =  CharField()

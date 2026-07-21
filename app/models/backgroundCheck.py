from app.models import *
from app.models.user import User
from app.models.term import Term
from app.models.backgroundCheckType import BackgroundCheckType

class BackgroundCheck(baseModel):
    user = ForeignKeyField(User)
    type = ForeignKeyField(BackgroundCheckType)
    backgroundCheckStatus = CharField()
    dateCompleted = DateField(null=True)
    deletionDate = DateTimeField(null=True)
    deletedBy = TextField(null=True)
    termSubmitted = ForeignKeyField(Term)

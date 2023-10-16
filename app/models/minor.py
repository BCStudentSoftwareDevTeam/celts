from app.models import*
from app.models.minorReqsComplete import MinorReqsComplete
from app.models.term import Term
from app.models.user import User

class Minor(baseModel):
    user = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    minorReqsComplete = ForeignKeyField(MinorReqsComplete)
    isInterested = BooleanField(default = False)

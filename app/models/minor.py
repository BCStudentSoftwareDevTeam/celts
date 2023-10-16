from app.models import*
from app.models.minorRequirements import MinorReqs
from app.models.term import Term
from app.models.user import User

class Minor(baseModel):
    user = ForeignKeyField(User)
    term = ForeignKeyField(Term)
    minorReqs = ForeignKeyField(MinorReqs)
    isInterested = BooleanField(default = False)

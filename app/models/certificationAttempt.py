from app.models import *
from app.models.certification import Certification
from app.models.user import User
from app.models.term import Term
import datetime

class CertificationAttempt(baseModel):
    certification = ForeignKeyField(Certification)
    user = ForeignKeyField(User)
    dateStarted = DateField(default=datetime.datetime.now)
    termStarted = ForeignKeyField(Term)
    dateEnded = DateField(null=True)
    endReason = CharField(null=True)

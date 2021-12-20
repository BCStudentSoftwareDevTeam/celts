from app.models import*
from app.models.user import User
from app.models.outsideParticipant import OutsideParticipant

class MatchParticipants(baseModel):
    volunteer = ForeignKeyField(User)
    outsideParticipant = ForeignKeyField(OutsideParticipant)

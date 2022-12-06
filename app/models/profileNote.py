from app.models import *
from app.models.user import User
from app.models.note import Note

class ProfileNote(baseModel):
    user = ForeignKeyField(User)
    note = ForeignKeyField(Note, null=False)
    isBonnerNote = BooleanField(default=False)
    viewTier = IntegerField(default=3)

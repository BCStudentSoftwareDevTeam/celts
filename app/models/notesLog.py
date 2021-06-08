from app.models import*
from app.models.user import User

class NotesLog(baseModel):
    noteID = PrimaryKeyField()
    createdBy = ForeignKeyField(User)
    createdOn = Date()
    noteContent = CharField()
    isPrivate = Boolean(default=False)

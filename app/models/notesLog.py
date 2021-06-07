from app.models import*
from app.models.user import User

class NotesLog(baseModel):
    noteID = PrimaryKeyField()
    createdBy = ForeignKeyField(User, null=False)
    createdOn = Date(null=False)
    noteContent = CharField(null=False)
    isPrivate = Boolean(null=True)

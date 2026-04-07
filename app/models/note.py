from app.models import*
from app.models.user import User

class Note(baseModel):
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField()
    noteContent = TextField()
    isPrivate = BooleanField(default=False)
    noteType = CharField(null=True)

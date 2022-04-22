from app.models import *
from app.models.program import Program
from app.models.user import User
from app.models.note import Note

class ProgramBan(baseModel):
    user = ForeignKeyField(User)
    program = ForeignKeyField(Program)
    endDate = DateField(null=True)
    banNote = ForeignKeyField(Note, null=False)
    unbanNote = ForeignKeyField(Note, null=True)

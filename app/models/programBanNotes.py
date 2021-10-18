from app.models import *
from app.models.programBan import ProgramBan
from app.models.note import Note

class ProgramBanNotes(baseModel):
    programBan = ForeignKeyField(ProgramBan)
    note = ForeignKeyField(Note, backref="notes")

    class Meta:
        primary_key=CompositeKey('programBan', 'note')

from app.models import *
from app.models.program import Program

class Training(baseModel):
    name = CharField()
    description = TextField(null=True)
    program = ForeignKeyField(Program)
    hasNoProgram = BooleanField(default=False)
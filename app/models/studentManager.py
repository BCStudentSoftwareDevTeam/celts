from app.models import *
from app.models.program import Program
from app.models.user import User

class StudentManager(baseModel):
    user = ForeignKeyField(User)
    program = ForeignKeyField(Program)

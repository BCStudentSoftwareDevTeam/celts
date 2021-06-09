from app.models import*
from app.models.program import Program
from app.models.user import User

class Interest(baseModel):
    program = ForeignKeyField(Program)
    user = ForeignKeyField(User)

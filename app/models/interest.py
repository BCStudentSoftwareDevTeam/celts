from app.models import*
from app.models.program import Program
from app.models.user import User

class Interest(baseModel):
    interestID = PrimaryKeyField()
    program = ForeignKeyField(Program)
    user = ForeignKeyField(User)

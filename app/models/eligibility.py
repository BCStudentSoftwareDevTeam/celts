from app.models import*
from app.models.user import User
from app.models.program import Program

class Eligibility(baseModel):
    eligibilityID = PrimaryKeyField()
    user = ForeignKeyField(User)
    program = ForeignKeyField(Program)

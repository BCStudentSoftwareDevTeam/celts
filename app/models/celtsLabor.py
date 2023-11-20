from app.models import * 
from app.models.user import User
from app.models.term import Term

class CeltsLabor(baseModel):
    user = ForeignKeyField(User)
    positionTitle = CharField()
    term = ForeignKeyField(Term)
    isAcademicYear = BooleanField(default=False)

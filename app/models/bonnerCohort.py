from app.models import *
from app.models.user import User

class BonnerCohort(baseModel):
    year = IntegerField()
    user = ForeignKeyField(User)

    class Meta:
        indexes = ( (('year','user'), True), )

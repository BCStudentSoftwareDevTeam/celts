from app.models import *
from app.models.user import User

class BonnerYear(baseModel):
    year = IntegerField()
    user = ForeignKeyField(User)

    class Meta:
        primary_key=CompositeKey('year', 'user')

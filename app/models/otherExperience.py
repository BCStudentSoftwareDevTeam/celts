from app.models import *
from app.models.term import Term
from app.models.user import User

class OtherExperience(baseModel):
    user = ForeignKeyField(User)
    activity = CharField()
    term = ForeignKeyField(Term)
    hours = IntegerField()
    weeks = IntegerField()
    service = CharField()
    company = CharField()

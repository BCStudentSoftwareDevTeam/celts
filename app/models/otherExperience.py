from app.models import *
from app.models.term import Term

class OtherExperience(baseModel):
    activity = CharField()
    term = ForeignKeyField(Term)
    hours = IntegerField()
    weeks = IntegerField()
    service = CharField()
    company = CharField()

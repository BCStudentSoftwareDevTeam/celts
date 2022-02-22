from app.models import *

class Term(baseModel):
    description = CharField()
    year = IntegerField()
    academicYear = CharField()
    isSummer = BooleanField(default=False)
    isCurrentTerm = BooleanField(default=False)

from app.models import *

class Term(baseModel):
    description = CharField()
    year = IntegerField()
    academicYear = CharField()
    isBreak = BooleanField(default=False)
    isSummer = BooleanField(default=False)
    isCurrentTerm = BooleanField(default=False)

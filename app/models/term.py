from app.models import*

class Term(baseModel):
    termID = PrimaryKeyField()
    termName = CharField()
    year = CharField()
    academicYear = CharField()

from app.models import*

class Term(baseModel):
    termID = PrimaryKeyField()
    termName = CharField(null=False)
    year = CharField(null=False)
    academicYear = CharField(null=False)

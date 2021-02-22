class Term:
    termID = PrimaryKeyField()
    termName = CharField(null=False)
    year = CharField(null=False)
    academicYear = CharField(null=False)

class NotesLog:
    noteID = PrimaryKeyField()
    createdBy_id = ForeignKeyField(null=False)
    createdOn = Date(null=False)
    noteContent = CharField(null=False)
    isPrivate = Boolean(null=True)

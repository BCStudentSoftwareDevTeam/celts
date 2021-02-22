class OutsideParticipant:
    outsideParticipantID = PrimaryKeyField()
    event_id = ForeignKeyField(null=False)
    firstName = CharField(null=False)
    lastName = CharField(null=False)
    email = CharField(null=False)
    phoneNumber = CharField(null=False)

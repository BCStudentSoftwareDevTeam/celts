class EventParticipant:
    participantID = PrimaryKeyField()
    user_id = ForeignKeyField(null=False)
    event_id = ForeignKeyField(null=False)
    hoursEarned = CharField(null=True)

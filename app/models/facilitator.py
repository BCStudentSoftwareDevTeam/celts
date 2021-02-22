class Facilitator:
    facilitatorID = PrimaryKeyField()
    user_id = ForeignKeyField(null=False)
    event_id = ForeignKeyField(null=False)

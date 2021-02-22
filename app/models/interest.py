class Interest:
    interestID = PrimaryKeyField()
    program_id = ForeignKeyField(null=False)
    user_id = ForeignKeyField(null=False)

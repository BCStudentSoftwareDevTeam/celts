class Eligibility:
    eligibilityID = PrimaryKeyField()
    user_id = ForeignKeyField(null=False)
    program_id = ForeignKeyField(null=False)

class CourseParticipant:
    trackedHoursID = PrimaryKeyField()
    course_id = ForeignKeyField(null=False)
    user_id = ForeignKeyField(null=False)
    hoursEarned = CharField(null=False)

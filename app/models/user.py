from app.models import*

class User(baseModel):
    userID = PrimaryKeyField()
    bnumber = CharField()
    email = CharField()
    phoneNumber = CharField()
    firstName = CharField()
    lastName  = CharField()
    isStudent = BooleanField(default=False)
    isFaculty = BooleanField(default=False)
    isCeltsAdmin = BooleanField(default=False)
    isCeltsStudentStaff = BooleanField(default=False)

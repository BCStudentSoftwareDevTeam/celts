from app.models import*

class User(baseModel):
    userID = PrimaryKeyField()
    bnumber = CharField(null=False)
    email = CharField(null=False)
    phoneNumber = CharField(null=False)
    firstName = CharField(null=False)
    lastName  = CharField(null=False)
    isStudent = BooleanField(null=True)
    isFaculty = BooleanField(null=True)
    isCeltsAdmin = BooleanField(null=True)
    isCeltsStudentStaff = BooleanField(null=True)

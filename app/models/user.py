from app.models import*

class User(baseModel):
    username = CharField(primary_key=True)
    bnumber = CharField(unique=True)
    email = CharField()
    phoneNumber = CharField()
    firstName = CharField()
    lastName  = CharField()
    isStudent = BooleanField(default=False)
    isFaculty = BooleanField(default=False)
    isCeltsAdmin = BooleanField(default=False)
    isCeltsStudentStaff = BooleanField(default=False)

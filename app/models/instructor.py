from sqlalchemy import VARCHAR
from app.models import*

class Instructor(baseModel):
    username = CharField(primary_key=True)
    bnumber = CharField(unique=True)
    email = CharField()
    phoneNumber = CharField()
    firstName = CharField()
    lastName  = CharField()
  
    

    # @property
    # def isAdmin(self):
    #     return (self.isCeltsAdmin or self.isCeltsStudentStaff)

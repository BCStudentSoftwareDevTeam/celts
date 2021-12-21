from app.models import*

class AllOutsideParticipants(baseModel):
    email = CharField(primary_key=True)
    firstName = CharField()
    lastName = CharField()
    phoneNumber = CharField()

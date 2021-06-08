from app.models import*

class Partner(baseModel):
    partnerID = PrimaryKeyField()
    partnerName = CharField()

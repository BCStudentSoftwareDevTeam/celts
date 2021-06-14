from app.models import*
from app.models.partner import Partner

class Program(baseModel):
    programName = CharField()
    partner = ForeignKeyField(Partner, null=True)

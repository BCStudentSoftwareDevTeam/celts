from app.models import*
from app.models.partner import Partner

class Program(baseModel):
    programName = PrimaryKeyField()
    partner = ForeignKeyField(Partner, null=False)

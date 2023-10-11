from app.models import * 
from app.models.user import User

class CeltsLabor(baseModel):
    user = ForeignKeyField(User)
    positionTitle = CharField()
    termName = CharField()

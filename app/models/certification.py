from app.models import *
from app.models.user import User

class Certification(baseModel):
    name = CharField()
    isArchived = BooleanField(default=False)

    BONNER = 1
    CESC = 2

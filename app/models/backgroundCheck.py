from app.models import *
from app.models.user import User

class BackgroundCheck(baseModel):
    user = ForeignKeyField(User)
    passBackgroundCheck = BooleanField(default=False)

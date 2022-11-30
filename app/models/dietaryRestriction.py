from app.models import *
from app.models.user import User

class DietaryRestriction(baseModel):
    user = ForeignKeyField(User)
    dietRestriction = TextField()

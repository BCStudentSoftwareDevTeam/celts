from app.models import *
from app.models.user import User
from app.models.backgroundCheckType import BackgroundCheckType

class BackgroundCheck(baseModel):
    user = ForeignKeyField(User)
    type = ForeignKeyField(BackgroundCheckType)
    passBackgroundCheck = BooleanField(default=False)
    datePassed = DateField(null=True)

    class Meta:
        primary_key=CompositeKey('user', 'type')

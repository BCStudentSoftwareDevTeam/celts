from app.models import *

class BackgroundCheckType(baseModel):
    id = CharField(primary_key=True)
    description = CharField()

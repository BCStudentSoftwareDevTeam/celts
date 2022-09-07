from app.models import *


class EmailTemplate(baseModel):
    subject = CharField()
    body = CharField()
    action = CharField()
    purpose = CharField()
    replyToAddress = CharField()

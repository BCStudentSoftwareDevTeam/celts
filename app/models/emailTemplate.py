from app.models import*

class EmailTemplate(baseModel):
    subject = CharField()
    body = TextField()
    action = CharField()
    purpose = CharField()
    replyToAddress = CharField()

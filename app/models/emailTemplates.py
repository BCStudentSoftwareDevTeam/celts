from app.models import*

class EmailTemplate(baseModel):
    emailTemplateID = PrimaryKeyField()
    subject = CharField()
    body = CharField()
    action = CharField()
    purpose = CharField()
    replyToAddress = CharField()

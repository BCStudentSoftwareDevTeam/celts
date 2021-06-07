from app.models import*

lass EmailTemplate(baseModel):
    emailTemplateID = PrimaryKeyField()
    subject = CharField(null=False)
    body = CharField(null=False)
    action = CharField(null=False)
    purpose = CharField(null=False)
    replyToAddress = CharField(null=False)

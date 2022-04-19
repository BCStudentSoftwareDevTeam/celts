from app.models import*
from app.models.emailTemplate import EmailTemplate
from app.models.event import Event

class EmailLog(baseModel):
    event = ForeignKeyField(Event)
    templateUsed = ForeignKeyField(EmailTemplate, null=True)
    subject = CharField()
    body = TextField()
    recipientsCategory = CharField()
    recipients = CharField()
    dateSent = DateTimeField()

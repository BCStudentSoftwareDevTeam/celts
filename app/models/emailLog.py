from app.models import*
from app.models.emailTemplate import EmailTemplate
from app.models.event import Event

class EmailLog(baseModel):
    event = ForeignKeyField(Event)
    subject = CharField()
    templateUsed = ForeignKeyField(EmailTemplate, null=True)
    recipientsCategory = CharField()
    recipients = CharField()
    dateSent = DateTimeField()

from app.models import *
from app.models.emailTemplate import EmailTemplate 
from app.models.event import Event 
from app.models.user import User

class EmailLog(baseModel):
    event = ForeignKeyField(Event)
    subject = CharField()
    templateUsed = ForeignKeyField(EmailTemplate)
    recipientsCategory = CharField()
    recipients = CharField()
    dateSent = DateTimeField()
    sender = CharField()
    attachmentName = CharField(null=True)

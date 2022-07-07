from app.models import*
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
    sender = ForeignKeyField(User)
<<<<<<< HEAD
    attachmentFullPath = CharField(null=True)
=======
    attachmentName = CharField()
>>>>>>> 9879f1e39c590d5dc2c5b13e0a647cbfa06cb07c

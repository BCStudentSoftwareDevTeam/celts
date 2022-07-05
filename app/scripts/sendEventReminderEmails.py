from app.logic.emailHandler import EmailHandler
from app.models.event import Event
from app.models.term import Term
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.user import User
from app.models.emailTemplate import EmailTemplate
from peewee import DoesNotExist
from datetime import date, datetime, timedelta

def checkForEvents():
    try:
        tomorrowDate = date.today() + timedelta(days=1)
        currentTerm = Term.select(Term.id).where(Term.isCurrentTerm==1)
        events = list(Event.select().where(Event.startDate==tomorrowDate))
        template = EmailTemplate.get(purpose = "Reminder")
        templateSubject = template.subject
        templateBody = template.body
        for event in events:
            programId = event.singleProgram
            senderName = programId.emailSenderName
            emailData = {"eventID":event.id,
                            "programID":programId,
                            "term":currentTerm,
                            "templateIdentifier":"Reminder",
                            "recipientsCategory":"Interested",
                            "senderName":senderName,
                            "subject":templateSubject,
                            "body":templateBody}
            sendEmail = EmailHandler(emailData, "172.31.3.239:8080", User.get_by_id("ramsayb2"))
            sendEmail.send_email()

    except (DoesNotExist, IndexError) as e:
        print(e)
def main():
    checkForEvents()

main()

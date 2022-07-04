from app.logic.emailHandler import EmailHandler
from app.models.event import Event
from app.models.term import Term
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.user import User
from app.models.emailTemplate import EmailTemplate
from datetime import date, datetime, timedelta

def checkForEvents():
    tomorrowDate = date.today() + timedelta(days=1)
    currentTerm = Term.select(Term.id).where(Term.isCurrentTerm==1)
    events = list(Event.select().where(Event.startDate==tomorrowDate))

    template = EmailTemplate.get(purpose = "Reminder")
    templateSubject = template.subject
    templateBody = template.body
    for event in events:
        programId = event.singleProgram
        senderName = Program.get(Program.emailSenderName)
        emailData = {"EventId":event.id,
                        "ProgramId":programId,
                        "term":currentTerm,
                        "purpose":"Reminder",
                        "recipientsCategory":"Interested",
                        "senderName":senderName,
                        "subject":templateSubject,
                        "body":templateBody}
        sendEmail = EmailHandler(emailData, "172.31.2.2:8080", User.get_by_id("ramsayb2"))
        sendEmail.send_email()

def main():
    checkForEvents()

main()

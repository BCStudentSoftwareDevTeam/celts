from app.logic.emailHandler import EmailHandler
from app.models.event import Event
from app.models.term import Term
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.user import User
from app.models.emailTemplate import EmailTemplate
from datetime import date, datetime, timedelta

def checkForEvents():
    currentDate = date.today().strftime("%m/%d/%Y")
    today = datetime.strptime(currentDate,"%m/%d/%Y")
    tomorrowDate = today + timedelta(days=1)
    currentTerm = Term.select(Term.id).where(Term.isCurrentTerm==1)
    events = list(Event.select().where(Event.startDate==tomorrowDate))
    template = EmailTemplate.select().where(EmailTemplate.purpose == "Reminder").dicts()
    templateSubject = template[0]['subject']
    templateBody = template[0]['body']
    for i in range(len(events)):
        programId = ProgramEvent.select(ProgramEvent.program).where(Program.event==events[i].id)
        senderName = Program.get(Program.senderName)
        emailData = {"EventId":events[i].id,
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

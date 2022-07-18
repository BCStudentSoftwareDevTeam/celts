from app.logic.emailHandler import EmailHandler
from app.logic.events import getTomorrowsEvents
from app.models.term import Term
from app.models.user import User
from app.models.emailTemplate import EmailTemplate

def sendAutomatedEmail(events):
    """Function that sends an email for every event occuring the next day"""
    if not len(events):
        print("No events were found.")
        return 0
    counter = 0
    currentTerm = Term.get(isCurrentTerm=1)
    template = EmailTemplate.get(purpose = "Reminder")
    templateSubject = template.subject
    templateBody = template.body
    for event in events:
        programId = event.singleProgram
        emailData = {"eventID":event.id,  # creates the email data
                        "programID":programId,
                        "term":currentTerm.id,
                        "templateIdentifier":"Reminder",
                        "recipientsCategory":"Interested",
                        "subject":templateSubject,
                        "body":templateBody}
        sendEmail = EmailHandler(emailData, "172.31.3.239:8080", User.get_by_id("ramsayb2"))
        sendEmail.send_email()
        counter+=1
    return counter

def main():
    sendAutomatedEmail(getTomorrowsEvents())

main()

import os
import socket

from app import app
from app.logic.emailHandler import EmailHandler
from app.logic.events import getTomorrowsEvents
from app.models.term import Term
from app.models.user import User
from app.models.emailTemplate import EmailTemplate

def sendEventReminderEmail(events):
    """Function that sends an email for every event occuring the next day"""
    if not len(events):
        return 0

    counter = 0
    currentTerm = Term.get(isCurrentTerm=1)

    template = EmailTemplate.get(purpose = "Reminder")
    templateSubject = template.subject
    templateBody = template.body
    for event in events:
        programId = event.program
        emailData = {"eventID":event.id,  # creates the email data
                     "programID":programId,
                     "term":currentTerm.id,
                     "emailSender":"Reminder Automation",
                     "sender_name":"Reminder Automation",
                     "templateIdentifier":"Reminder",
                     "recipientsCategory":"Interested",
                     "subject":templateSubject,
                     "body":templateBody}
        sendEmail = EmailHandler(emailData, gethost())
        sendEmail.send_email()
        counter += 1
    return counter

def main():
    sendEventReminderEmail(getTomorrowsEvents())

def gethost():
    host = "localhost:8080"
    if os.getenv('IP'):
        host = os.getenv('IP') + ":" + os.getenv('PORT')
    else:
        host = socket.gethostbyname(socket.gethostname()) + ":8080"

    if app.env == "production":
        host = socket.getfqdn()

    return host

# main()

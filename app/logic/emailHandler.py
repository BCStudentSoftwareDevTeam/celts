from flask import Flask, request, render_template, redirect, url_for
import yaml, os
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.program import Program
from app.models.eventParticipant import EventParticipant
from app.models.emailTemplate import EmailTemplate
from app import app
import sys
import webbrowser
import time
from pathlib import Path

"""
The Requirements:
1. Send Email - Components:- Sender, Receiver, Email Body
2. Edit Email - Management Page
3. Create recipients groups? - Would they ever create manual groups for anything?
   - If so, where would we save this? A new table?
   - Q: will they send emails to individuals???

TODO:

- A general method that sets up the connection (would this need to be called when email is sent?)

- Method to receive all the info needed: Sender, Receiver, email_topic, etc.
  - This method will also clean up the data so it can be used in other methods.

- Method to retrieve email_template
  - What should be the parameter for retrieval? Not the subject. We should find a better identifies.

- Method to update email_template (after admin edits the tempate this method could be called).
  - We could check which field(s) needs update in this method. Or create a new one.

- Method to send the email.

- Methods to get the email addresses of all categories (To), such as interested/participating etc.
  - How many categories/groups will be there?

 - Method to replace_fields in email_template
   - things like recipient name, event name, description, date and time
   - Come up with a smart way to do this.
   - This can be called inside send_email method, or another method called before that.
     because at that point we should have all the fields info

Notes:
- All the backend logic/processing should happen in the Email Handler class.
  For instance, the code in /events/email.py can be all moved to the class.
  So that in email.py, we only do one or two function calls.

- Email Handler class shouldn't be dependent on form data.
  It should have a method that receives data (could be in any one format),
  cleans it up. Then other methods will use it.

- Why is the updateSenderEmail updating config? Instead of updating config,
  the class can have variables that hold sender, receiver, etc. info.
  first it will fetch from the config. If need updated, then the variable alone would be updated.
"""

def getInterestedEmails(listOfPrograms):

    """ Gets emails of students interested in a program. """
    emails = []

    volunteersToEmail = User.select(User.email).join(Interest).join(Program, on=(Program.id == Interest.program)).where(Program.id.in_([p.id for p in listOfPrograms]))

    return [user.email for user in volunteersToEmail]

def getParticipantEmails(eventID = None):
    """ Gets emails of students participating in an event. """
    volunteersToEmail = User.select().join(EventParticipant).where(EventParticipant.event == eventID)
    return [user.email for user in volunteersToEmail]

class emailHandler():
    """ A class for email setup and configuring the correct data to send. """
    def __init__(self, application, emailInfo):
        self.emailInfo = emailInfo
        self.application = application
        self.mail = Mail(self.application)


    def updateSenderEmail(self, message):
        """ Updates who is sending the emails based on the event_list form. """
        if self.emailInfo['emailSender'] == 'CELTS Admins':
            app.config.update(
                MAIL_USERNAME = app.config['admin_username'],
                MAIL_PASSWORD = app.config['admin_password']
            )
            message.sender = app.config['admin_username']

        elif self.emailInfo['emailSender'] == 'CELTS Student Staff':
            app.config.update(
                MAIL_USERNAME = app.config['staff_username'],
                MAIL_PASSWORD = app.config['staff_password']
            )
            message.sender = app.config['staff_username']
        return message

    def sendEmail(self, msg: Message, emails):
        """ Updates the sender and sends the email. """
        message = self.updateSenderEmail(msg)

        # Q: What's the difference between these two?
        if 'sendIndividually' in self.emailInfo:
            if app.config.mail['MAIL_OVERRIDE_ALL']:
                message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
            with self.mail.connect() as conn:
                for email in emails:
                    message.recipients = [email]
                    conn.send(message)
        else:
            try:
                if app.config['ENV'] == 'testing':
                    message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
                message.reply_to = app.config["MAIL_REPLY_TO_ADDRESS"]

                self.mail = Mail(app) # Q: Wasn't this already done in the constructor?
    # =======
    #             self.mail = Mail(self.application)
    # >>>>>>> f1383e327bd8d3176d911de02f37f61f6882329a
                self.mail.connect()
                self.mail.send(message)
            except:
                return False

        return True

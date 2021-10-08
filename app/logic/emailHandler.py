from flask import Flask, request, render_template
import yaml, os
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.emailTemplate import EmailTemplate
from app import app
import sys
from pathlib import Path

def getInterestedEmails(programID = None):
    """ Gets emails of students interested in a program. """
    volunteersToEmail = User.select().join(Interest).where(Interest.program == programID)
    return [user.email for user in volunteersToEmail]

def getParticipantEmails(eventID = None):
    """ Gets emails of students participating in an event. """
    volunteersToEmail = User.select().join(EventParticipant).where(EventParticipant.event == eventID)
    return [user.email for user in volunteersToEmail]

class emailHandler():
    """ A class for email setup and configuring the correct data to send. """
    def __init__(self, emailInfo):

        self.emailInfo = emailInfo
        self.mail = Mail(app)
        self.mail.connect()

    def updateSenderEmail(self):
        """ Updates who is sending the emails based on the event_list form. """
        if '@' in self.emailInfo['emailSender']: #if the current user is sending the email
            pass

        elif self.emailInfo['emailSender'] == 'CELTS Admins':
            app.config.update(
                MAIL_USERNAME= app.config['mail']['admin_username'],
                MAIL_PASSWORD = app.config['mail']['admin_password']
            )
            print("\n\n"+app.config["MAIL_USERNAME"])

        elif self.emailInfo['emailSender'] == 'CELTS Student Staff':
            app.config.update(
                MAIL_USERNAME= app.config['mail']['staff_username'],
                MAIL_PASSWORD= app.config['mail']['staff_password']
            )

    def sendEmail(self, message: Message, emails):
        """ Updates the sender and sends the email. """
        self.updateSenderEmail()
        if 'sendIndividually' in self.emailInfo:
            if app.config['MAIL_OVERRIDE_ALL']:
                message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
            with self.mail.connect() as conn:
                for email in emails:
                    message.recipients = [email]
                    conn.send(message)
        else:
            if app.config['MAIL_OVERRIDE_ALL']:
                message.recipients = [app.config['MAIL_OVERRIDE_ALL']]

            message.reply_to = app.config["REPLY_TO_ADDRESS"]
            self.mail.send(message)
        return 1

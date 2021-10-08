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
#
# def load_config(file):
#     """ Loads the 'default' file in the config directory. """
#     with open(file, 'r') as ymlfile:
#         cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
#     return cfg

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
        # self.default = load_config('app/config/default.yml')
        # app.config.update(
        #     MAIL_SERVER=self.default['mail']['server'],
        #     MAIL_PORT=self.default['mail']['port'],
        #     # MAIL_USERNAME= default['mail']['username'],
        #     # MAIL_PASSWORD= default['mail']['password'],
        #     REPLY_TO_ADDRESS= self.default['mail']['reply_to_address'],
        #     MAIL_USE_TLS=self.default['mail']['tls'],
        #     MAIL_USE_SSL=self.default['mail']['ssl'],
        #     MAIL_DEFAULT_SENDER=self.default['mail']['default_sender'],
        #     MAIL_OVERRIDE_ALL=self.default['mail']['override_addr']
        # )

        self.emailInfo = emailInfo
        self.mail = Mail(app)
        self.mail.connect()

    def updateSenderEmail(self):
        """ Updates who is sending the emails based on the event_list form. """
        if '@' in self.emailInfo['emailSender']: #if the current user is sending the email
            pass
            # app.config.update(
            # MAIL_USERNAME= self.emailInfo['emailSender'],
            # # MAIL_PASSWORD= ??????       # how do you get the password???
            #)
        elif self.emailInfo['emailSender'] == 'CELTS Admins':
            app.config.update(
                MAIL_USERNAME= self.default['mail']['admin_username'],
                MAIL_PASSWORD = self.default['mail']['admin_password']
            )
            print("\n\n"+app.config["MAIL_USERNAME"])

        elif self.emailInfo['emailSender'] == 'CELTS Student Staff':
            app.config.update(
                MAIL_USERNAME= self.default['mail']['staff_username'],
                MAIL_PASSWORD= self.default['mail']['staff_password']
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

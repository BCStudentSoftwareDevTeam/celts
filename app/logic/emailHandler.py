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

def load_config(file):
    """ This should be in a seperate file. prob in the config dir"""
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


def getVolunteerEmails(programID = None, eventID = None, emailRecipients = "interested"):
    """
    gets the emails of all the students who are interested in a program or are participating in an event.
    """
    if emailRecipients == 'interested':    #email all students interested in the program
        volunteersToEmail = User.select().join(Interest).where(Interest.program == programID)

    elif emailRecipients == 'eventParticipant':  #email only people who rsvped
        volunteersToEmail = User.select().join(EventParticipant).where(EventParticipant.event == eventID)

    else:
        print("ITS IMPRESSIVE HOW YOU MANAGED TO BREAK THIS")
    return [user.email for user in volunteersToEmail]


class emailHandler():
    def __init__(self, emailInfo):
        default = load_config('app/config/default.yml')
        app.config.update(
            MAIL_SERVER=default['mail']['server'],
            MAIL_PORT=default['mail']['port'],
            MAIL_USERNAME= default['mail']['username'],
            MAIL_PASSWORD= default['mail']['password'],
            REPLY_TO_ADDRESS= default['mail']['reply_to_address'],
            MAIL_USE_TLS=default['mail']['tls'],
            MAIL_USE_SSL=default['mail']['ssl'],
            MAIL_DEFAULT_SENDER=default['mail']['default_sender'],
            MAIL_OVERRIDE_ALL=default['mail']['override_addr']
        )
        self.emailInfo = emailInfo
        self.mail = Mail(app)

    def sendEmail(self, message: Message, emails):
        try:
            if 'sendIndividually' in self.emailInfo:    #<-----------------------need to test this some more.
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

        except:
            return 0

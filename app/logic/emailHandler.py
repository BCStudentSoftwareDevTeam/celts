from flask import Flask, request, render_template, redirect, url_for
import yaml, os
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.emailTemplate import EmailTemplate
from app import app
import sys
import webbrowser
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
    def __init__(self, mail, emailInfo):
        app.config.update(
            MAIL_SERVER=app.config['mail']['server'],
            MAIL_PORT=app.config['mail']['port'],
            MAIL_USERNAME= app.config['mail']['admin_username'],
            MAIL_PASSWORD= app.config['mail']['admin_password'],
            REPLY_TO_ADDRESS= app.config['mail']['reply_to_address'],
            MAIL_USE_TLS=app.config['mail']['tls'],
            MAIL_USE_SSL=app.config['mail']['ssl'],
            #MAIL_DEFAULT_SENDER=app.config['mail']['default_sender'],
            #ALWAYS_SEND_MAIL=default['ALWAYS_SEND_MAIL']
            MAIL_OVERRIDE_ALL=app.config['mail']['override_addr']
        )
        self.emailInfo = emailInfo
        self.mail = mail
        self.mail.connect()
    def updateSenderEmail(self, message):
        """ Updates who is sending the emails based on the event_list form. """

        if self.emailInfo['emailSender'] == 'CELTS Admins':
            message.sender = app.config['mail']['admin_username']

        elif self.emailInfo['emailSender'] == 'CELTS Student Staff':
            message.sender = app.config['mail']['staff_username']

        return message

    def sendEmail(self, message: Message, emails):
        """ Updates the sender and sends the email. """
        message = self.updateSenderEmail(message)
        # print(f'\n{message.sender},\n{message.subject}')
        # if '@' in self.emailInfo['emailSender']: #if the current user is sending the email
        #     msg = self.emailInfo['message'].replace(" ",'%20')
        #     subject = self.emailInfo['subject'].replace(" ",'%20')
        #     if app.config['mail']['override_addr']:
        #         recipients = app.config['mail']['override_addr']
        #     else:
        #         recipients = emails
        #     webbrowser.open_new(f'mailto:?to={recipients}&subject={subject}&body={msg}')
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

            message.reply_to = app.config['mail']["reply_to_address"]
            self.mail.send(message)
        return 1

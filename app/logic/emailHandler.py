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
import time
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

        if app.config['MAIL_OVERRIDE_ALL']:
            message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
        message.reply_to = app.config["REPLY_TO_ADDRESS"]

        self.mail = Mail(app)
        self.mail.connect()
        self.mail.send(message)

        return 1

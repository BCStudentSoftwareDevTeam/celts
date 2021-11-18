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

def getInterestedEmails(listOfPrograms):
    """ Gets emails of students interested in a program. """
    emails = []
    print("\n\n\n\n\n",listOfPrograms,"\n\n\n\n\n")

    volunteersToEmail = User.select(User.email).join(Interest).join(Program, on=(Program.id == Interest.program)).where(Program.id.in_([p.id for p in listOfPrograms]))
    print("\n\n\n\n\n",volunteersToEmail,"\n\n\n\n\n")
    print("\n\n\n\n\n", volunteersToEmail.objects(),"\n\n\n\n\n")

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
        try:
            if app.config['ENV'] == 'testing':
                message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
            message.reply_to = app.config["MAIL_REPLY_TO_ADDRESS"]

            self.mail = Mail(self.application)
            self.mail.connect()
            self.mail.send(message)
        except:
            return False

        return True

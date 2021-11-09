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
import urllib.parse
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

def useMailTo(emailInfo, recipients):
    """ opens a new tab/window for the user to send email (using outllok, gmail, etc.)
        populates the from, to, subject, and body fields with the email the User wants to send"""
    print(f"""\n using mail to \n sender: {urllib.parse.quote(emailInfo['emailSender'])} \n recipients: {recipients}
    subject: {urllib.parse.quote(emailInfo['subject'])} \n body: {urllib.parse.quote(emailInfo['message'])} \n""")
    subject = urllib.parse.quote(emailInfo['subject'])
    body = urllib.parse.quote(emailInfo['message'])
    emailRecipients = ",".join(recipients)
    print(f"\n recipients {emailRecipients}\n")

    mailtoLink = f"mailto:{emailRecipients}?subject={subject}&body={body}"
    print("\n HERE \n ")
    print(f"\n {mailtoLink} \n")
    webbrowser.open_new(mailtoLink)

    time.sleep(2)

    return 1


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

        if 'sendIndividually' in self.emailInfo:
            if app.config.mail['MAIL_OVERRIDE_ALL']:
                message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
            with self.mail.connect() as conn:
                for email in emails:
                    message.recipients = [email]
                    conn.send(message)
        else:
            if app.config['MAIL_OVERRIDE_ALL']:
                message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
            message.reply_to = app.config["REPLY_TO_ADDRESS"]

            self.mail = Mail(app)
            self.mail.connect()
            self.mail.send(message)

        return 1

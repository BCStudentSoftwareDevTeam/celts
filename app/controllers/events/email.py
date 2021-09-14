from flask import Flask, redirect, flash, url_for, request, g
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.emailHandler import getVolunteerEmails, emailHandler
from app.controllers.events import events_bp
from app import app

@events_bp.route('/email', methods=['POST'])
def emailVolunteers():

    emailInfo = request.form
    emails = getVolunteerEmails(emailInfo['programID'], emailInfo['eventID'], emailInfo['emailRecipients'])
    mail = emailHandler(emailInfo)
    emailSent = mail.sendEmail(Message(emailInfo['subject'], emails, emailInfo['message']), emails)
    if emailSent == 1:
        flash("Email successfully sent!", "success")
    else:
        flash("Error sending email", "danger")

    return redirect(url_for("events.events", term = 1))

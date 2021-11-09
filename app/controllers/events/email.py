from flask import Flask, redirect, flash, url_for, request, g
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.emailHandler import *
from app.controllers.events import events_bp
from app import app

@events_bp.route('/email', methods=['POST'])
def emailVolunteers():
    """ Uses emailHandler to send an email with the form in event_list. """
    emailInfo = request.form

    if emailInfo['emailRecipients'] == "interested":
        emails = getInterestedEmails(emailInfo['programID'])
    elif emailInfo['emailRecipients'] == "eventParticipant":
        emails = getParticipantEmails(emailInfo['eventID'])
    else:
        flash("Unable to determine email recipients", "danger")

    if emails == None:
        flash("Error getting email recipients", "danger")
        return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))

    if '@' in emailInfo['emailSender']:
        emailSent = useMailTo(emailInfo, emails)

    else:
        email = emailHandler(emailInfo)
        emailSent = email.sendEmail(Message(emailInfo['subject'],
                                           emails, # recipients
                                           emailInfo['message']),
                                           emails) # passed for sending individually
    if emailSent == 1:
        flash("Email successfully sent!", "success")
    else:
        flash("Error sending email", "danger")
    return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))

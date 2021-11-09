from flask import Flask, redirect, flash, url_for, request, g
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.logic.emailHandler import getInterestedEmails, getParticipantEmails, emailHandler
from app.models.programEvent import ProgramEvent
from app.controllers.events import events_bp
from app import app

@events_bp.route('/email', methods=['POST'])
def emailVolunteers():
    """ Uses emailHandler to send an email with the form in event_list. """

    emailInfo = request.form.copy()
    if '@' in emailInfo['emailSender']: # if they are using mailto instead
        return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))
    else:
        if emailInfo['programID'] == 'Unknown':
            program = ProgramEvent.get(ProgramEvent.event == emailInfo['eventID'])
            emailInfo['programID'] = program.id

        if emailInfo['emailRecipients'] == "interested":
            emails = getInterestedEmails(emailInfo['programID'])
        elif emailInfo['emailRecipients'] == "eventParticipant":
            emails = getParticipantEmails(emailInfo['eventID'])
        else:
            flash("Unable to determine email recipients", "danger")

        if emails == None:
            flash("Error getting email recipients", "danger")
            return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))

        email = emailHandler(app,emailInfo)
        emailSent = email.sendEmail(Message(emailInfo['subject'],
                                           emails, # recipients
                                           emailInfo['message']),
                                           emails) # passed for sending individually
        if emailSent == 1:
            flash("Email successfully sent!", "success")
        else:
            flash("Error sending email", "danger")
        return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))

@events_bp.route('/mailto', methods=['POST'])
def getEmails(emailGroup, programID=None, eventID=None):
    """asdfs"""

    if emailGroup=='interested' and programID:
        emails = getInterestedEmails(programID)

    elif emailGroup == 'eventParticipant' and eventID:
        email = getInterestedEmails(eventID)

    else:
        flash("Unable to determine email recipients", "danger")

    return email

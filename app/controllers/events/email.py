from flask import Flask, redirect, flash, url_for, request, g, render_template
from flask_mail import Mail, Message
from peewee import fn
from app.models.interest import Interest
from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.controllers.main import main_bp
from app.logic.emailHandler import getInterestedEmails, getParticipantEmails, emailHandler
from app import app

@main_bp.route('/retrieveEmailTemplate', methods=['GET'])
def retrieveEmailTemplate():
    # Couldn't find a way to do this with render_template
    # TODO: find a better way?
    templateInfo = {}
    emailTemplates = EmailTemplate.select()

    for index, template in enumerate(emailTemplates):
        templateInfo[index] = {
            'purpose': template.purpose,
            'subject':template.subject,
            'body': template.body}
    return templateInfo

@main_bp.route('/fetchEmailLogData/<eventId>', methods=['GET'])
def fetchEmailLogData(eventId):
    dateSent = recipients = None
    # TODO: Bruteforce implementation. Need to figure out a way to get the most recent email log for an event
    emailLogs = EmailLog.select().where(EmailLog.event==eventId).order_by(EmailLog.dateSent.asc())
    for emailLog in emailLogs:
        recipients = emailLog.recipientsCategory
        dateSent = emailLog.dateSent.strftime('%m/%d/%Y')
    return {'recipients':recipients, 'dateSent':dateSent}


# @events_bp.route('/email', methods=['POST'])
def emailVolunteers():
    """ Uses emailHandler to send an email with the form in event_list. """

    emailInfo = request.form.copy()
    if '@' in emailInfo['emailSender']: # if they are using mailto instead
        return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))
    else:
        if emailInfo['programID'] == 'Unknown':
            programs = ProgramEvent.select(ProgramEvent.program).where(ProgramEvent.event == emailInfo['eventID'])
            listOfPrograms = [program.program for program in programs.objects()]
            emailInfo['programID'] = listOfPrograms
        if emailInfo['recipients'] == "interested":
            emails = getInterestedEmails(emailInfo['programID'])
        elif emailInfo['recipients'] == "eventParticipant":
            emails = getParticipantEmails(emailInfo['eventID'])

        if emails == None:
            flash("Error getting email recipients", "danger")
            return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))

        email = emailHandler(app,emailInfo)
        emailSent = email.sendEmail(Message(emailInfo['subject'],
                                           emails, # recipients
                                           emailInfo['body']),
                                           emails) # passed for sending individually
        if emailSent == True:
            flash("Email successfully sent!", "success")
        else:
            flash("Error sending email", "danger")
        return redirect(url_for("main.events", selectedTerm = emailInfo['selectedTerm']))

# @events_bp.route('/mailto', methods=['POST'])
def getEmails(emailGroup, programID=None, eventID=None):
    """This is where the ajax call should get the mailto info"""

    if emailGroup=='interested' and programID:
        emails = getInterestedEmails(programID)

    elif emailGroup == 'eventParticipant' and eventID:
        email = getInterestedEmails(eventID)

    else:
        flash("Unable to determine email recipients", "danger")

    return email

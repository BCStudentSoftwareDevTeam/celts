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

# TODO: Do we still need this?
# @main_bp.route('/mailto', methods=['POST'])
def getEmails(emailGroup, programID=None, eventID=None):
    """This is where the ajax call should get the mailto info"""

    if emailGroup=='interested' and programID:
        emails = getInterestedEmails(programID)

    elif emailGroup == 'eventParticipant' and eventID:
        email = getInterestedEmails(eventID)

    else:
        flash("Unable to determine email recipients", "danger")

    return email

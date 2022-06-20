from app.models.emailTemplate import EmailTemplate
from flask import g
from urllib.parse import urlparse
from app.models.emailLog import EmailLog
from app.controllers.main import main_bp
from app.logic.emailHandler import EmailHandler

@main_bp.route('/retrieveEmailTemplate', methods=['GET'])
def retrieveEmailTemplate():
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
    handle_last_email = EmailHandler(None, None, g.current_user)
    last_email = handle_last_email.retrieve_last_email(eventId)
    if last_email:
        return {'last_log': "The last email was sent to " + last_email.recipientsCategory + " on " + last_email.dateSent.strftime('%m/%d/%Y') + " by " + last_email.sender.email  + "." , 'last_log2': " Subject: " + last_email.subject}
    else:
        return {'exists': False}

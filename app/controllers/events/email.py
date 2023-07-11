from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.controllers.main import main_bp
from app.logic.emailHandler import EmailHandler
from app.models.program import Program
from flask import request

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

@main_bp.route('/retrievePlaceholderData', methods=['GET'])


@main_bp.route('/fetchEmailLogData/<eventId>', methods=['GET'])
def fetchEmailLogData(eventId):
    last_email = EmailHandler.retrieve_last_email(eventId)
    if last_email:
        return {'last_log': "The last email was sent to " + last_email.recipientsCategory + " on " + last_email.dateSent.strftime('%m/%d/%Y') + " by " + last_email.sender  + "." , 'last_log2': " Subject: " + last_email.subject}
    else:
        return {'exists': False}

@main_bp.route("/getProgramSender/", methods=['GET'])
def getProgramSender():
    programId = request.args.get("programId")
    return Program.get_by_id(programId).contactName

from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.controllers.main import main_bp
from app.logic.emailHandler import EmailHandler
from app.models.program import Program
from flask import request

@main_bp.route('/retrieveSenderList/<eventId>', methods=['GET'])
def retrieveSenderList(eventId): # Beans: get the program managers based on the eventId. Also get the correct program email using the eventId

    programOption = ["Adopt A Grandparent (agp@berea.edu)", "agp"]
    studentStaffOptions = [
        ["Bob (bob@berea.edu)", "bob"],
        ["Steve (steve@berea.edu)", "steve"]
    ]
    return [
        ["CELTS (celts@berea.edu)", "celts"],
        programOption,
        *studentStaffOptions
        ]


@main_bp.route('/retrieveEmailTemplate/<eventId>', methods=['GET'])
def retrieveEmailTemplate(eventId):
    templateInfo = {}
    emailTemplates = EmailTemplate.select()

    for index, template in enumerate(emailTemplates):
        templateInfo[index] = {
            'purpose': template.purpose,
            'subject':template.subject,
            'body': EmailHandler.replaceStaticPlaceholders(eventId, template.body)
            }
    return templateInfo

@main_bp.route('/retrievePlaceholderList/<eventId>', methods=['GET'])
def retrievePlaceholderList(eventId):
    return EmailHandler.retrievePlaceholderList(eventId)


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

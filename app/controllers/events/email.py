from app.models.emailTemplate import EmailTemplate
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
    last_email = EmailHandler.retrieve_last_email(eventId)
    if last_email != None:
        return {'last_log': "The last email was sent to " + last_email.recipientsCategory + " on " + last_email.dateSent.strftime('%m/%d/%Y') + " by " + last_email.sender.email  + "." , 'last_log2': " Subject: " + last_email.subject}
        # {'recipients':last_email.recipientsCategory,'dateSent': last_email.dateSent.strftime('%m/%d/%Y'),'subject':last_email.subject,'sender':last_email.sender.email}


    # if (EmailLog.select().where(EmailLog.event==eventId)).exists():
    #     emailLog = EmailLog.select().where(EmailLog.event==eventId).order_by(EmailLog.dateSent.desc()).get()
    #     return {'recipients': emailLog.recipientsCategory, 'dateSent': emailLog.dateSent.strftime('%m/%d/%Y')}
    else:
        return {'exists': False}

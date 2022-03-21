from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.controllers.main import main_bp

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
    if (EmailLog.select().where(EmailLog.event==eventId)).exists():
        emailLog = EmailLog.select().where(EmailLog.event==eventId).order_by(EmailLog.dateSent.desc()).get()
        return {'recipients': emailLog.recipientsCategory, 'dateSent': emailLog.dateSent.strftime('%m/%d/%Y')}
    return {'exists': False}

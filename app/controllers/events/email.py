from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.models.event import Event
from app.controllers.main import main_bp
from app.logic.emailHandler import EmailHandler
from app.models.program import Program
from flask import request, flash, g, redirect, url_for
from urllib.parse import urlparse

@main_bp.route('/email', methods=['POST'])
def email():
    raw_form_data = request.form.copy()
    attachments = request.files.getlist('attachmentObject')
    if "@" in raw_form_data['emailSender']:
        # when people are sending emails as themselves (using mailto) --- Q: are we still going with the mailto option?
        pass
    else:
        url_domain = urlparse(request.base_url).netloc
        mail = EmailHandler(raw_form_data, url_domain, attachment_file=attachments)
        mail_sent = mail.send_email()

        if mail_sent:
            message, status = 'Email successfully sent!', 'success'
        else:
            message, status = 'Error sending email', 'danger'
        flash(message, status)
        return redirect(url_for("main.events", selectedTerm = raw_form_data['selectedTerm']))


@main_bp.route('/retrieveSenderList/<eventId>', methods=['GET'])
def retrieveSenderList(eventId):
    senderOptions = [["CELTS (celts@berea.edu)", "Celts"]]

    event = Event.get_by_id(eventId)
    if event.program_id:
        programEmail = event.program.contactEmail if event.program.contactEmail else "No Program Email Found"
        programOption = [f"{event.program.programName} ({programEmail})", event.program.programName]
        senderOptions.append(programOption)

    studentStaffOptions = []
    senderOptions.extend(studentStaffOptions)

    currentUserOption = [f"Current User ({g.current_user.email})", g.current_user.username]
    senderOptions.append(currentUserOption)

    return senderOptions


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

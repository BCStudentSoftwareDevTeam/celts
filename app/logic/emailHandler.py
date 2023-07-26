from datetime import datetime
from peewee import DoesNotExist, JOIN
from flask_mail import Mail, Message, Attachment
import os

from app import app
from app.models.interest import Interest
from app.models.user import User
from app.models.program import Program
from app.models.eventRsvp import EventRsvp
from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.term import Term

class EmailHandler:
    def __init__(self, raw_form_data, url_domain, attachment_file=[]):

        self.mail = Mail(app)
        self.raw_form_data = raw_form_data
        self.url_domain = url_domain
        self.override_all_mail = app.config['MAIL_OVERRIDE_ALL']
        self.sender_username = None
        self.sender_name = None
        self.sender_address = None
        self.reply_to = app.config['MAIL_REPLY_TO_ADDRESS']
        self.template_identifier = None
        self.subject = None
        self.body = None
        self.event = None
        self.program = None
        self.recipients = None
        self.sl_course_id = None
        self.attachment_path = app.config['files']['base_path'] + app.config['files']['email_attachment_path']
        self.attachment_filepaths = []
        self.attachment_file = attachment_file

    def process_data(self):
        """ Processes raw data and stores it in class variables to be used by other methods """
        # Email Template Data
        # Template Identifier
        if 'templateIdentifier' in self.raw_form_data:
            self.template_identifier = self.raw_form_data['templateIdentifier']

        if 'subject' in self.raw_form_data:
            self.subject = self.raw_form_data['subject']

        # Event
        if 'eventID' in self.raw_form_data:
            event = Event.get_by_id(self.raw_form_data['eventID'])
            self.event = event

        # Program
        if self.event:
            self.program = self.event.program

        if 'emailSender' in self.raw_form_data:
            self.sender_username = self.raw_form_data['emailSender']
            self.sender_name, self.sender_address, self.reply_to = self.getSenderInfo()

        if 'body' in self.raw_form_data:
            self.body = self.raw_form_data['body']

        # Recipients
        if 'recipientsCategory' in self.raw_form_data:
            self.recipients_category = self.raw_form_data['recipientsCategory']
            self.recipients = self.retrieve_recipients(self.recipients_category)

        # Service-Learning Course
        if 'slCourseId' in self.raw_form_data:
            self.sl_course_id = self.raw_form_data['slCourseId']

    def getSenderInfo(self):
        programObject = Program.get_or_none(Program.programName == self.sender_username)
        userObj = User.get_or_none(User.username == self.sender_username)
        senderInfo = [None, None, None]
        if programObject:
            programEmail = programObject.contactEmail
            senderInfo = [programObject.programName, programEmail, programEmail]
        elif self.sender_username.upper() == "CELTS":
            senderInfo = ["CELTS", "celts@berea.edu", "celts@berea.edu"]
        elif userObj:
            senderInfo = [f"{userObj.fullName}", userObj.email, userObj.email]
        # overwrite the sender info with intentional keys in the raw form data.
        get = self.raw_form_data.get
        senderInfo = [get('sender_name') or senderInfo[0], get('sender_address') or senderInfo[1], get('reply_to') or senderInfo[2]]

        return senderInfo # If the email is not being sent from a program or user, use default values.

    def update_sender_config(self):
        # We might need this.
        # This functionality should be moved somewhere else.
        # The function in another file would receive email_info[sender]
        # and update the config based on that and wherever we will end up saving emails and passwords
        #The sender information should be saved like so: {"name": [email, password], } or in the database
        pass

    def retrieve_recipients(self, recipients_category):
        """ Retrieves recipient based on which category is chosen in the 'To' section of the email modal """
        # Other potential recipients:
        # - course instructors
        # - course Participants
        # - outside participants'
        if recipients_category == "Interested":
            recipients = (User.select()
                .join(Interest)
                .join(Program, on=(Program.id==Interest.program))
                .where(Interest.program == self.program))
        if recipients_category == "RSVP'd":
            recipients = (User.select()
                .join(EventRsvp)
                .where(EventRsvp.event==self.event.id))

        if recipients_category == "Eligible Students":
            # all terms with the same accademic year as the current term,
            # the allVolunteer training term then needs to be in that query
            Term2 = Term.alias()
            
            sameYearTerms = Term.select().join(Term2, on=(Term.academicYear == Term2.academicYear)).where(Term2.isCurrentTerm == True)

            bannedUsers = ProgramBan.select(ProgramBan.user).where((ProgramBan.endDate > datetime.now()) | (ProgramBan.endDate is None), ProgramBan.program == (self.program if self.program else ProgramBan.program))
            allVolunteer = Event.select().where(Event.isAllVolunteerTraining == True, Event.term.in_(sameYearTerms))
            recipients = User.select().join(EventParticipant).where(User.username.not_in(bannedUsers), EventParticipant.event.in_(allVolunteer))
        return list(recipients)



    def replaceDynamicPlaceholders(self, email_body, *, name):
        """ Replaces placeholders that cannot be predetermined on the front-end """
        event_link = f"{self.url_domain}/event/{self.event.id}/view"
        new_body = email_body.format(recipient_name=name, event_link=event_link)
        return new_body

    def retrieve_and_modify_email_template(self):
        """ Retrieves email template based on idenitifer and calls replace_general_template_placeholders"""

        email_template = EmailTemplate.get(EmailTemplate.purpose==self.template_identifier) # --Q: should we keep purpose as the identifier?
        template_id = email_template.id
        
        body = EmailHandler.replaceStaticPlaceholders(self.event.id, self.body)

        self.reply_to = email_template.replyToAddress
        return (template_id, self.subject, body)

    def getAttachmentFullPath(self, newfile=None):
        """
        This creates the directory/path for the object from the "Choose File" input in the emailModal.html file.
        :returns: directory path for attachment
        """
        attachmentFullPath = None
        try:
            # tries to create the full path of the files location and passes if
            # the directories already exist or there is no attachment
            attachmentFullPath = os.path.join(self.attachment_path, newfile.filename)
            if attachmentFullPath[:-1] == self.attachment_path:
                return None
            os.mkdir(self.attachment_path)

        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError: # will pass if the file already exists
            pass
        return attachmentFullPath

    def saveAttachment(self):
        """ Saves the attachment in the app/static/files/attachments/ directory """
        try:
            for file in self.attachment_file:
                attachmentFullPath = self.getAttachmentFullPath(newfile = file)
                if attachmentFullPath:
                    file.save(attachmentFullPath) # saves attachment in directory
                    self.attachment_filepaths.append(attachmentFullPath)

        except AttributeError: # will pass if there is no attachment to save
            pass

    def store_sent_email(self, subject, template_id):
        """ Stores sent email in the email log """
        date_sent = datetime.now()

        attachmentNames = []
        for file in self.attachment_file:
            attachmentNames.append(file.filename)

        EmailLog.create(
            event = self.event.id,
            subject = subject,
            templateUsed = template_id,
            recipientsCategory = self.recipients_category,
            recipients = ", ".join(recipient.email for recipient in self.recipients),
            dateSent = date_sent,
            sender = self.sender_username,
            attachmentNames = attachmentNames)

    def build_email(self):
        # Most General Scenario
        self.saveAttachment()
        self.process_data()
        template_id, subject, body = self.retrieve_and_modify_email_template()
        return (template_id, subject, body)

    def send_email(self):
        defaultEmailInfo = {"senderName":"CELTS", "replyTo":app.config['celts_admin_contact'], "senderAddress":app.config['celts_admin_contact']} 
        template_id, subject, body = self.build_email()

        attachmentList = []
        for i, filepath in enumerate(self.attachment_filepaths):
            with app.open_resource(filepath[4:]) as file:
                attachmentList.append(Attachment(filename=filepath.split('/')[-1], content_type=self.attachment_file[i].content_type, data=file.read()))

        try:
            with self.mail.connect() as conn:
                for recipient in self.recipients:
                    full_name = f'{recipient.firstName} {recipient.lastName}'
                    email_body = self.replaceDynamicPlaceholders(body, name=full_name)
                    conn.send(Message(
                        subject,
                        # [recipient.email],
                        [self.override_all_mail],
                        email_body,
                        attachments = attachmentList,
                        reply_to = self.reply_to or defaultEmailInfo["replyTo"],
                        sender = (self.sender_name or defaultEmailInfo["senderName"], self.sender_address or defaultEmailInfo["senderAddress"])
                    ))
            self.store_sent_email(subject, template_id)
            return True
        except Exception as e:
            print("Error on sending email: ", e)
            return False

    def update_email_template(self):
        try:
            self.process_data()
            (EmailTemplate.update({
                EmailTemplate.subject: self.subject,
                EmailTemplate.body: self.body,
                EmailTemplate.replyToAddress: self.reply_to
            }).where(EmailTemplate.purpose==self.template_identifier)).execute()
            return True
        except Exception as e:
            print("Error updating email template record: ", e)
            return False

    def retrieve_last_email(event_id):
        try:
            last_email = EmailLog.select().where(EmailLog.event==event_id).order_by(EmailLog.dateSent.desc()).get()
            return last_email
        except DoesNotExist:
            return None
  

    @staticmethod
    def retrievePlaceholderList(eventId):
        event = Event.get_by_id(eventId)
        return [
            ["Recipient Name", "{recipient_name}"],
            ["Event Name", event.name],
            ["Start Date", (event.startDate).strftime('%m/%d/%Y')],
            ["End Date", (event.endDate).strftime('%m/%d/%Y')],
            ["Start Time", (event.timeStart).strftime('%I:%M')],
            ["End Time", (event.timeEnd).strftime('%I:%M')],
            ["Location", event.location],
            ["Event Link", "{event_link}"],
            ["Relative Time", event.relativeTime]
        ]

    @staticmethod
    def replaceStaticPlaceholders(eventId, email_body):
        """ Replaces all template placeholders except for those that can't be known until just before Send-time """
        event = Event.get_by_id(eventId)

        new_body = email_body.format(event_name=event.name,
                                     location=event.location,
                                     start_date=(event.startDate).strftime('%m/%d/%Y'),
                                     end_date=(event.endDate).strftime('%m/%d/%Y'),
                                     start_time=(event.timeStart).strftime('%I:%M'),
                                     end_time=(event.timeEnd).strftime('%I:%M'),
                                     event_link="{event_link}",
                                     recipient_name="{recipient_name}",
                                     relative_time=event.relativeTime)
        return new_body
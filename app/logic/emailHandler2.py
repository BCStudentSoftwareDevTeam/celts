
from app.models.programEvent import ProgramEvent



class EmailHandler:
    def __init__(self, raw_form_data):
        # Q: Can we send email without accessing config?
        # We need config to set up server connection and store all email addresses and passwords.
        self.mail = Mail(app)
        self.raw_form_data = raw_form_data
        self.sender = app.config['admin_username']
        self.override_all_mail = app.config.mail['MAIL_OVERRIDE_ALL']
        self.recipients = None
        self.program_ids = None
        self.event_id = None
        self.service_learning_course_id = None
        self.template_identifier = None

    # --------------- sending functionality
    def process_data(self):
        """ Processes raw data and stores it in class variables to be used by other methods """

        if "@" in self.raw_form_data['emailSender']:
            # when people are sending emails as themselves (using mailto) --- Q: are we still going with the mailto option?
            pass
        else:
            self.template_identifier = self.raw_form_data['templateIdentifier']

            if 'serviceLearningCourseId' in self.raw_form_data:   #if this email is for a service learning course
                self.service_learning_course_id = self.raw_form_data['serviceLearningCourseId']

            # I removed the "else" because some service learning courses are tied to events and programs.
            # TODO: Need to handle the above edge case
            self.event_id = self.raw_form_data['eventId']
            fetch_event_programs() # -- Q: We need to decide what needs to be rertuned by functions and what needs to be stored in class variables

        pass

    def fetch_event_programs(self):
        """ Fetches all the programs of a particular event """
        # Non-student-led programs have "Unknown" as their id ---Q: maybe this id should be changed to something more specific?
        if self.raw_form_data['programId'] == 'Unknown':
            # One event can have multiple programs -- Q: Is this true only for non-student-led events?
            programs = ProgramEvent.select(ProgramEvent.program).where(ProgramEvent.event==self.event_id)
            self.program_ids = [program.program for program in programs.objects()]
        else:
            self.program_ids = [self.raw_form_data['programId']]

    def update_sender_config(self):
        # We might need this.
        pass


    def retrieve_recipients(self):
        # retrieves email addresses of different groups:
        # 1. Participants
        # 2. Intested.
        # 3. RSVP'd
        # 4. course instructors
        # 5. course Participants
        # 6. outside participants

        # recipient_emails = User.select().query()
        self.recipients = [recipient.email for recipient in recipients_emails]

    def replace_general_template_placholders(self, template_body):
        # the email template will have placeholders for fields like
        # recipient name, event name, date and time???, sender's name?
        # This would need to be called in retrieve_email_template method
        # before it returns the email_template

        # Implement this in a smart way.
        # One idea: template.format(name, event_name)

        # Q: for loop through the emails? Or search bcc??
        new_template = template_body.format(date=date, event, name)
        return new_template

    def replace_name_placeholder(self, name, email_body):
        # new_email_body = email_body.format(name=name)
        return new_email_body

    def retrieve_and_modify_email_template(self):  # --rename
    """ retrieves email template based on idenitifer and calls replace_general_template_placholders"""
        # retrieves email template based on an idenitifer
        # what should the identifier be?
        template = EmailTemplate.get(jjj)
        new_body = self.replace_general_template_placholders(template.body)

        return (template.subject, new_body, template.reply_to)

    def attach_attachments(self):
        # TODO for later
        # retrieve attachments, attach it to the email
        # Q: how would this work?
        pass

    def build_email(self):
        # Most General Scenario
        process_data()
        retrieve_recipients()
        subject, body, reply_to = retrieve_and_modify_email_template()

        return (subject, body, reply_to)

    def send_email(self):
        subject, body, reply_to = build_email()
        # contains only the sending functionality
        with self.mail.connect() as conn:
            for recipient in self.recipients:
                email_body = replace_name_placeholder(recipient.name, body)

                conn.send(Message(
                    subject,
                    [recipient.email],
                    email_body,
                    reply_to=reply_to
                ))

    # ------------- management functionality
    def update_email_template(self):
        pass

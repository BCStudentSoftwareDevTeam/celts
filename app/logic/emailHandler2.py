
from app.models.programEvent import ProgramEvent



class EmailHandler:
    def __init__(self, email_info):
        # Q: Will email_info always be a form? Yes
        # Q: Can we send email without accessing config?
        self.email_info = email_info # raw_email_form_data  --- rename
        self.mail = Mail(app)
        self.email_sender = app.config.mail['email']
        self.recipients
        self.reply_to
        self.override_all_mail = app.config.mail['MAIL_OVERRIDE_ALL'] #? default

        #
        self.program_ids    #changed this to be plural because an event could have multiple programs
        self.event_id
        self.course_id
        self.template_identifier

    # --------------- sending functionality
    def process_data(self):
        # clean up email_info to be used in other methods
        # Q/A: Check for correctness of data/datatype??
        # - check for email addresses -- @
        # set up class variables

        if "@" in self.email_info['emailSender']:
            # when people are sending emails as themselves (using mailto)
            pass
        else:

            if 'courseID' in self.email_info:   #if this email is for a service learning course
                self.course_id = self.email_info['courseID']
            else:
                self.event_id = self.email_info['eventID']

                #This logic should prob be in a seperate file/function, but where?
                #This gets all the programs for a particular event
                if self.email_info['programID'] == 'Unknown': #the programId is "Unknown" for all non-studentLedPrograms
                    programs = ProgramEvent.select(ProgramEvent.program).where(ProgramEvent.event == self.event_id)
                    self.program_ids = [program.program for program in programs.objects()]  #this must be a list because there will be multiple programs for an event.
                else:
                    self.program_ids = [self.email_info['programID']] #keeping this as a list so that we don't have to handel two forms of self.program_Id

            self.template_identifier = self.email_info['template']
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

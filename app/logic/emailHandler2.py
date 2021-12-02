

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
        self.program_id
        self.event_id
        self.course_id
        self.template_identifier

    # --------------- sending functionality
    def process_data(self):
        # clean up email_info to be used in other methods
        # Q/A: Check for correctness of data/datatype??
        # - check for email addresses -- @
        # set up class variables
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
        new_template = template_body.format(date=date, event name)
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

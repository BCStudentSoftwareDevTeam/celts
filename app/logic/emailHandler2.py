from flask_mail import Mail, Message
from app.models.programEvent import ProgramEvent
from app.models.interest import Interest
from app.models.user import User
from app.models.program import Program
from app.models.eventParticipant import EventParticipant
from app.models.emailTemplate import EmailTemplate
from app.models.event import Event
from app import app

class EmailHandler:
    def __init__(self, raw_form_data):
        self.mail = Mail(app)
        self.raw_form_data = raw_form_data
        self.override_all_mail = app.config['MAIL_OVERRIDE_ALL']
        self.template_identifier = None
        self.program_ids = None
        self.event_id = None
        self.sl_course_id = None # service learning course
        self.recipients = None

    # --------------- sending functionality
    def process_data(self):
        """ Processes raw data and stores it in class variables to be used by other methods """
        self.template_identifier = self.raw_form_data['templateIdentifier']
        self.subject = self.raw_form_data['subject'] if 'subject' in self.raw_form_data else None
        self.body = self.raw_form_data['body'] if 'body' in self.raw_form_data else None
        self.program_ids = self.fetch_event_programs(self.raw_form_data['programID'])
        self.event_id = self.raw_form_data['eventID'] if 'eventID' in self.raw_form_data else None
        self.sl_course_id = self.raw_form_data['slCourseId'] if 'slCourseId' in self.raw_form_data else None
        self.recipients = self.retrieve_recipients(self.raw_form_data["recipientsCategory"])

    def fetch_event_programs(self, programId):
        """ Fetches all the programs of a particular event """
        # Non-student-led programs have "Unknown" as their id
        # ---Q: maybe this id should be changed to something more specific?
        if programId == 'Unknown':
            programs = ProgramEvent.select(ProgramEvent.program).where(ProgramEvent.event==self.event_id)
            return [program.program for program in programs.objects()]
        else:
            program = ProgramEvent.get_by_id(programId)
            return [program.program]

    def update_sender_config(self):
        # We might need this.
        # This functionality should be moved somewhere else.
        # The function in another file would receive email_info[sender]
        # and update the config based on that and wherever we will end up saving emails and passwords
        #The sender information should be saved like so: {"name": [email, password], } or in the database
        pass

    def retrieve_recipients(self, recipients_category):
        """ Retrieves recipient based on which category is chosen in the 'To' section of the email modal """
        # retrieves email addresses of different groups:
        # - course instructors
        # - course Participants
        # - outside participants
        if recipients_category == "interested":
            recipients = (User.select()
                .join(Interest)
                .join(Program, on=(Program.id==Interest.program))
                .where(Program.id.in_([p.id for p in self.program_ids])))

        if recipients_category == "eventParticipant":
            recipients = (User.select()
                .join(EventParticipant)
                .where(EventParticipant.event==self.event_id))

        return [recipient for recipient in recipients]

    def replace_general_template_placholders(self, email_body=None):
        event_link = "event/<self.event_id>" # how are we generating this?
        event = Event.get_by_id(self.event_id)

        new_body = email_body.format(event_name=event.name,
            location=event.location,
            start_date=event.startDate, # TODO: need to format the dates and times
            end_date=event.endDate,
            start_time=event.timeStart,
            end_time=event.timeEnd,
            event_link=event_link,
            name="{name}")
        return new_body

    def replace_name_placeholder(self, name, body):
        new_body = body.format(name=name)
        return new_body

    def retrieve_and_modify_email_template(self):
        """ retrieves email template based on idenitifer and calls replace_general_template_placholders"""

        template_body = EmailTemplate.get(EmailTemplate.purpose==self.template_identifier)

        subject = self.subject if self.subject else template_body.subject

        body = self.body if self.body else template_body.body
        new_body = self.replace_general_template_placholders(body)

        reply_to = template_body.replyToAddress
        return (subject, new_body, reply_to)

    def attach_attachments(self):
        # TODO for later
        # retrieve attachments, attach it to the email
        # Q: how would this work?
        pass

    def build_email(self):
        # Most General Scenario
        self.process_data()
        subject, body, reply_to = self.retrieve_and_modify_email_template()
        return (subject, body, reply_to)

    def send_email(self):
        subject, body, reply_to = self.build_email()
        try:
            with self.mail.connect() as conn:
                for recipient in self.recipients:
                    full_name = f'{recipient.firstName} {recipient.lastName}'
                    email_body = self.replace_name_placeholder(full_name, body)

                    conn.send(Message(
                        subject,
                        # [recipient.email],
                        [self.override_all_mail],
                        email_body,
                        reply_to=reply_to,
                        sender = ("Sandesh", 'bramsayr@gmail.com')
                    ))
            return True
        except Exception as e:
            print("Error on sending email: ", e)
            return False

    # ------------- management functionality
    def update_email_template(self):
        pass

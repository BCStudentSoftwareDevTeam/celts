import pytest
from flask_mail import Message
from app.logic.emailHandler2 import EmailHandler
from app import app

# Q: Should we test each method as well?
@pytest.mark.integration
def test_email_handler():
    with app.app_context():
        # Case 1: Send email with subject and body -- as if email is sent using a modal
        raw_form_data = {"templateIdentifier": "Test",
            "subject": "Test Email",
            "body": "Hello {name}",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "interested"}

        app.config.update(
            MAIL_SUPRESS_SEND = True
        )

        email = EmailHandler(raw_form_data)

        with email.mail.record_messages() as outbox:
            email_sent = email.send_email()
            assert email_sent == True

            assert len(outbox) == 2
            assert outbox[0].subject == "Test Email"
            assert outbox[0].body == "Hello Sreynit Khatt"

        # Case 2: Send email without subject and body -- as if email is sent automatically
        raw_form_data = {"templateIdentifier": "Test",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "interested"}

        email_2 = EmailHandler(raw_form_data)

        with email_2.mail.record_messages() as outbox:
            email_sent = email_2.send_email()
            assert email_sent == True

            assert len(outbox) == 2
            assert outbox[0].subject == "Test Email"
            assert outbox[0].body == "Hello Sreynit Khatt,  This is a test event named Empty Bowls Spring Event 1 located in Seabury Center. Other info: 2021-10-12-2022-06-12 and this 18:00:00-21:00:00. The link is event/<self.event_id>"

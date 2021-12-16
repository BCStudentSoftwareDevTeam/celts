import pytest
from flask_mail import Message
from app import app
from app.models.emailTemplate import EmailTemplate
from app.logic.emailHandler2 import EmailHandler

@pytest.mark.integration
def test_send_email_using_modal():
    with app.test_request_context():

        app.config.update(
            MAIL_SUPRESS_SEND = True
        )
        # Case 1: Send email with subject and body -- as if email is sent using a modal
        raw_form_data = {"templateIdentifier": "Test",
            "subject": "Test Email",
            "body": "Hello {name}",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "Interested"}

        email = EmailHandler(raw_form_data)

        with email.mail.record_messages() as outbox:
            email_sent = email.send_email()
            assert email_sent == True

            assert len(outbox) == 2
            assert outbox[0].subject == "Test Email"
            assert outbox[0].body == "Hello Sreynit Khatt"

@pytest.mark.integration
def test_sending_automated_email():
    with app.test_request_context():
        # Case 2: Send email without subject and body -- as if email is sent automatically
        raw_form_data = {"templateIdentifier": "Test",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "Interested"}

        email = EmailHandler(raw_form_data)

        with email.mail.record_messages() as outbox:
            email_sent = email.send_email()
            assert email_sent == True

            assert len(outbox) == 2
            assert outbox[0].subject == "Test Email"
            assert outbox[0].body == "Hello Sreynit Khatt, This is a test event named Empty Bowls Spring Event 1 located in Seabury Center. Other info: 10/12/2021-06/12/2022 and this 06:00-09:00."

@pytest.mark.integration
def test_update_email_template():
    with app.test_request_context():
        raw_form_data = {"templateIdentifier": "Test2",
            "subject":"This is only a test",
            "body":"Hello {name}, Regards",
            "replyTo": "test.email@gmail.comm"}

        email = EmailHandler(raw_form_data)
        email.update_email_template()

        new_email_template = EmailTemplate.get(EmailTemplate.purpose==raw_form_data['templateIdentifier'])

        assert new_email_template.subject == raw_form_data['subject']
        assert new_email_template.body == raw_form_data['body']
        assert new_email_template.replyToAddress == raw_form_data['replyTo']

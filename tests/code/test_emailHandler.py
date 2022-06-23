import pytest
from flask_mail import Message
from urllib.parse import urlparse
from flask import request, g
from datetime import datetime
from dateutil import parser
import time
from app import app
from app.models.emailTemplate import EmailTemplate
from app.models.emailLog import EmailLog
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.logic.emailHandler import EmailHandler

@pytest.mark.integration
@pytest.mark.skip(reason="Authentication issues")
def test_send_email_using_modal():
    pass # For now we are skipping the email tests
    with app.test_request_context():

        app.config.update(
            MAIL_SUPRESS_SEND = True
        )
        with mainDB.atomic() as transaction:
            # Case 1: Send email with subject and body -- as if email is sent using a modal
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                "subject": "Test Email",
                "body": "Hello {name}",
                "programID":"1",
                "eventID":"1",
                "recipientsCategory": "Interested"}

            email = EmailHandler(raw_form_data, url_domain, User.get_by_id("neillz"))

            with email.mail.record_messages() as outbox:
                email_sent = email.send_email()
                assert email_sent == True

                assert len(outbox) == 2
                assert outbox[0].subject == "Test Email"
                assert outbox[0].body == "Hello Sreynit Khatt"

                transaction.rollback()

@pytest.mark.integration
@pytest.mark.skip(reason="Authentication issues")
def test_sending_automated_email():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            # Case 2: Send email without subject and body -- as if email is sent automatically
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                "programID":"1",
                "eventID":"1",
                "recipientsCategory": "Interested"}

            email = EmailHandler(raw_form_data, url_domain, User.get_by_id("neillz"))

            with email.mail.record_messages() as outbox:
                email_sent = email.send_email()
                assert email_sent == True

                assert len(outbox) == 2
                assert outbox[0].subject == "Test Email"
                assert outbox[0].body == "Hello Sreynit Khatt, This is a test event named Empty Bowls Spring Event 1 located in Seabury Center. Other info: 10/12/2021-06/12/2022 and this 06:00-09:00."

                transaction.rollback()

@pytest.mark.integration
@pytest.mark.skip(reason="Authentication issues")
def test_update_email_template():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test2",
                "subject":"This is only a test",
                "body":"Hello {name}, Regards",
                "replyTo": "test.email@gmail.comm"}

            email = EmailHandler(raw_form_data, url_domain, User.get_by_id("neillz"))
            email.update_email_template()

            new_email_template = EmailTemplate.get(EmailTemplate.purpose==raw_form_data['templateIdentifier'])

            assert new_email_template.subject == raw_form_data['subject']
            assert new_email_template.body == raw_form_data['body']
            assert new_email_template.replyToAddress == raw_form_data['replyTo']

            transaction.rollback()

@pytest.mark.integration
@pytest.mark.skip(reason="Authentication issues")
def test_email_log():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                "programID":"1",
                "eventID":"1",
                "recipientsCategory": "RSVP'd",
                "sender": User.get_by_id("ramsayb2")}

            email = EmailHandler(raw_form_data, url_domain, User.get_by_id("neillz"))

            with email.mail.record_messages() as outbox:
                email_sent = email.send_email()
                assert email_sent == True

            emailLog = EmailLog.get(EmailLog.event_id==1)
            assert emailLog.subject == "Test Email"
            assert emailLog.templateUsed_id == 1
            assert emailLog.recipientsCategory == "RSVP'd"
            time.sleep(.5) # Let's make sure that there is some separation in the times
            assert emailLog.dateSent <= datetime.now()

            rsvp_users = EventRsvp.select().where(EventRsvp.event_id==1)
            assert emailLog.recipients == ", ".join(user.user.email for user in rsvp_users)
            assert emailLog.sender == User.get_by_id("ramsayb2")
            transaction.rollback()

<<<<<<< HEAD
@pytest.mark.integration
def test_recipients_category():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                "programID":"3",
                "eventID":"1",
                "recipientsCategory": "Eligible Students"}

            testUserEmail = User.create( username="testuser",
                                    bnumber="B00000001",
                                    email="test@test.edu",
                                    phoneNumber="555-555-5555",
                                    firstName="Test",
                                    lastName="User",
                                    isFaculty="1")

            eventData =  {'isRsvpRequired':False, 'isService':False,
                          'isTraining':True, 'isRecurring':False, 'isAllVolunteerTraining':True, 'startDate': parser.parse('1999-12-12'),
                          'endDate':parser.parse('2022-06-12'), 'programId':1, 'location':"a big room",
                          'timeEnd':'21:00', 'timeStart':'18:00', 'description':"Empty Bowls Spring 2021",
                          'name':'Empty Bowls Spring Event 1','term':1,'facilitators':"ramsayb2"}

            Event.create(eventData)
            email = EmailHandler(raw_form_data, url_domain)
            email.process_data()

            target_results = [testUserEmail]

            assert email.recipients == target_results
            transaction.rollback()
=======

@pytest.mark.integration
def test_get_last_email():
    last_email = EmailHandler.retrieve_last_email(5)
    assert last_email.sender.username == "neillz"
    assert last_email.subject == "Time Change for {event_name}"
    assert last_email.templateUsed.subject == "Test Email 2"
    assert last_email.recipientsCategory == "RSVP'd"
    assert last_email.recipients == "ramsayb2"

    last_email = EmailHandler.retrieve_last_email(37)
    assert last_email is None
>>>>>>> 2eb1a1cef9584b393de65befc81b94ac41225591

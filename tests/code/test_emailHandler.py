import pytest
from flask_mail import Message
from urllib.parse import urlparse
from flask import request, g
from datetime import datetime, date
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
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.term import Term
from app.logic.emailHandler import EmailHandler

@pytest.mark.integration
def test_replaceStaticPlaceholders():
    body = EmailHandler.replaceStaticPlaceholders(1, "location= {location}, start_date= {start_date}, end_date= {end_date}, start_time= {start_time}, end_time= {end_time}")
    assert body == "location= Seabury Center, start_date= 10/12/2021, end_date= 06/12/2022, start_time= 06:00, end_time= 09:00"

    body = EmailHandler.replaceStaticPlaceholders(2, "location= {location}, start_date= {start_date}, end_date= {end_date}, start_time= {start_time}, end_time= {end_time}")
    assert body == "location= Berea Community School, start_date= 11/12/2021, end_date= 06/12/2022, start_time= 06:00, end_time= 09:00"
    
@pytest.mark.integration
def test_getSenderInfo():

    raw_form_data_list = []
    expected_sender_info_list = []
    
    # Adds program info
    raw_form_data_list.append({"emailSender": "Berea Buddies"})
    expected_sender_info_list.append(["Berea Buddies", "bereabuddies@berea.edu", "bereabuddies@berea.edu"])

    # Adds CELTS info
    raw_form_data_list.append({"emailSender": "celts"})
    expected_sender_info_list.append(["CELTS", "celts@berea.edu", "celts@berea.edu"])

    # Adds user info
    raw_form_data_list.append({"emailSender": "ramsayb2"})
    expected_sender_info_list.append(["Brian Ramsay", "ramsayb2@berea.edu", "ramsayb2@berea.edu"])

    # Adds program info
    raw_form_data_list.append({"emailSender": "RONALDDDDDDDDDDDDDDDDD"})
    expected_sender_info_list.append([None, None, None])

    for form_data, expected_sender_info in zip(raw_form_data_list, expected_sender_info_list):
        email = EmailHandler(form_data, "")

        email.process_data()

        assert email.getSenderInfo() == expected_sender_info
        assert email.sender_name == expected_sender_info[0]
        assert email.sender_address == expected_sender_info[1]
        assert email.reply_to == expected_sender_info[2]

    # tests to see that we can overwrite sender name address and the reply_to address
    raw_form_data = {"emailSender": "CELTS",
                     "sender_name": "i", 
                     "sender_address": "don't", 
                     "reply_to": "care"}

    email = EmailHandler(raw_form_data, "")
    email.process_data()
    assert email.sender_name == "i"
    assert email.sender_address == "don't"
    assert email.reply_to == "care"

@pytest.mark.integration
def test_send_email_using_modal():
    with app.test_request_context():


        with mainDB.atomic() as transaction:
            # Case 1: Send email with subject and body -- as if email is sent using a modal
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                             "emailSender": "neillz",
                             "subject": "Test Email",
                             "body": "Hello {recipient_name}",
                             "eventID":"1",
                             "recipientsCategory": "Interested"}

            email = EmailHandler(raw_form_data, url_domain)

            with email.mail.record_messages() as outbox:
                email_sent = email.send_email()
                assert email_sent == True

                assert len(outbox) == 2
                assert outbox[0].subject == "Test Email"
                assert outbox[0].body == "Hello Sreynit Khatt"

                transaction.rollback()
                

@pytest.mark.integration
def test_update_email_template():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test2",
                             "emailSender": "neillz",
                             "subject":"This is only a test",
                             "body":"Hello {recipient_name}, Regards"}

            email = EmailHandler(raw_form_data, url_domain)
            email.update_email_template()

            new_email_template = EmailTemplate.get(EmailTemplate.purpose==raw_form_data['templateIdentifier'])

            assert new_email_template.subject == raw_form_data['subject']
            assert new_email_template.body == raw_form_data['body']
            assert new_email_template.replyToAddress == "neillz@berea.edu"

            transaction.rollback()

@pytest.mark.integration
def test_email_log():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                             "emailSender": "ramsayb2",
                             "eventID":"1",
                             "subject":"Test Email",
                             "body":"We ran out of skeletons. Can you send some more?",
                             "recipientsCategory": "RSVP'd"}

            email = EmailHandler(raw_form_data, url_domain)

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
            assert emailLog.sender == "ramsayb2"
            transaction.rollback()

@pytest.mark.integration
def test_recipients_eligible_students():
    with app.test_request_context():
        with mainDB.atomic() as transaction:
            url_domain = urlparse(request.base_url).netloc
            raw_form_data = {"templateIdentifier": "Test",
                             "emailSender": 'ramsayb2',
                             "eventID":"3",
                             "recipientsCategory": "Eligible Students"}

            email = EmailHandler(raw_form_data, url_domain)
            email.process_data()
            assert email.recipients == []

            # Add partont to All Volunteer Training event: NOT banned and IS trained
            newTrainedStudent = EventParticipant.create(user = "partont", event = 14)
            email.process_data()
            assert email.recipients == [User.get_by_id("partont")]

            # Add ayisie to a non-all volunteer training event: NOT banned and NOT trained
            newTrainedStudent = EventParticipant.create(user = "ayisie", event = 5)
            email.process_data()
            assert email.recipients ==  [User.get_by_id("partont")]

            # Train ayisie so they show up in the results: NOT banned and IS trained
            newTrainedStudent = EventParticipant.create(user = "ayisie", event = 14)
            email.process_data()
            assert email.recipients ==  [User.get_by_id("partont"),User.get_by_id("ayisie")]
            newTrainedStudent.delete_instance()

            # Add khatts to All Volunteer Training event: IS banned and IS trained
            newTrainedStudent = EventParticipant.create(user = "khatts", event = 14)
            email.process_data()
            assert email.recipients == [User.get_by_id("partont")]
            newTrainedStudent.delete_instance()

            # Unban khatts while they have All Volunteer Training: NOT banned IS trained
            ProgramBan.update(endDate = parser.parser("2022-6-23")).where(ProgramBan.user == "khatts").execute()
            newTrainedStudent = EventParticipant.create(user = "khatts", event = 14)
            email.process_data()
            assert email.recipients == [User.get_by_id("partont"), User.get_by_id("khatts")]
            newTrainedStudent.delete_instance()

            # clearing data for the next test
            transaction.rollback()

            # Test a program that should have nothing in banned users and nothing in All Volunteer:
            raw_form_data = {"templateIdentifier": "Test",
                             "emailSender": 'ramsayb2',             
                             "eventID":"1",
                             "recipientsCategory": "Eligible Students"}

            email = EmailHandler(raw_form_data, url_domain)
            email.process_data()
            assert email.recipients == []

            # clearing data for the next test
            transaction.rollback()

            # Changed current term to next academic year while making training
            # occur in the previous academic year
            allVolunteerEvent = Event.get_by_id(14)
            newTrainedStudent = EventParticipant.create(user = "partont", event = allVolunteerEvent)

            raw_form_data = {"templateIdentifier": "Test",
                             "emailSender": 'ramsayb2',
                             "eventID":"1",
                             "recipientsCategory": "Eligible Students"}


            email = EmailHandler(raw_form_data, url_domain)
            email.process_data()
            assert email.recipients == [User.get_by_id("partont")]

            # Change the term that the All Volunteer Training takes place so that
            # it is in the past
            firstTerm = Term.select().order_by(Term.id).get()
            allVolunteerEvent.term = firstTerm
            allVolunteerEvent.save()

            # Update the current term in the database so that it is in the next
            # academic year
            Term.update(isCurrentTerm = False).where(Term.isCurrentTerm == True).execute()
            Term.update(isCurrentTerm = True).where(Term.id == 6).execute()

            email.process_data()
            assert email.recipients == []

            transaction.rollback()

@pytest.mark.integration
def test_get_last_email():
    last_email = EmailHandler.retrieve_last_email(5)
    assert last_email.sender == "neillz"
    assert last_email.subject == "Time Change for {event_name}"
    assert last_email.templateUsed.subject == "Test Email 2"
    assert last_email.recipientsCategory == "RSVP'd"
    assert last_email.recipients == "ramsayb2"

    last_email = EmailHandler.retrieve_last_email(37)
    assert last_email is None

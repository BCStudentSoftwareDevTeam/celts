import pytest
from flask_mail import Message
from app.logic.emailHandler import *
from app import app

#
# class emailHandler():
#     def __init__(self,)

@pytest.mark.integration
def test_getVolunteerEmails():

    programID = 1

    volunteerEmails = getInterestedEmails(programID)
    assert "bryanta@berea.edu" in volunteerEmails

    # check for non existing programId
    programID = 40
    volunteerEmails = getInterestedEmails(programID)

    assert volunteerEmails == []

    # invalid eventID
    programID = 1
    eventID = -1
    emailRecipients = "eventParticipant"

    volunteerEmails = getParticipantEmails(eventID)
    assert volunteerEmails == []
    volunteerEmails = getInterestedEmails(eventID)
    assert volunteerEmails == []

    # invalid recipients
    emailRecipients = 2
    volunteerEmails = getParticipantEmails(eventID)
    assert volunteerEmails == []

@pytest.mark.integration
def test_emailHandler():

    with app.app_context():
        emailInfo = {'emailSender': 'CELTS Admins'}
        app.config.update(
            TESTING = True,
            MAIL_SUPRESS_SEND = True
        )
        emails = getParticipantEmails(1)
        email = emailHandler(app,emailInfo)

        msg = Message("this email is for testing",
                      emails, # recipients
                      "Yup, just testing, don't look any closer.")

        #test updating sender
        updatedMsg = email.updateSenderEmail(msg)
        assert updatedMsg.sender == 'bramsayr@gmail.com'
        emailInfo['emailSender'] = "CELTS Student Staff"
        email.emailInfo = emailInfo
        updatedMsg = email.updateSenderEmail(msg)
        assert updatedMsg.sender == 'sceggenh@gmail.com'

        #test sending email
        with email.mail.record_messages() as outbox:
            emailSent = email.sendEmail(msg,emails) # passed for sending individually
            assert len(outbox) == 1;
            assert outbox[0].subject == "this email is for testing"
            assert outbox[0].body == "Yup, just testing, don't look any closer."
            if 'MAIL_OVERRIDE_ALL' in app.config:
                assert outbox[0].recipients == ["j5u6j9w6v1h0p3g1@bereacs.slack.com"]
            else:
                assert outbox[0].recipients == emails

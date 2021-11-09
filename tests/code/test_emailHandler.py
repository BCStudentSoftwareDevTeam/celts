import pytest
from flask_mail import Message
from app.logic.emailHandler import *
from app import app


class emailHandler():
    def __init__(self,)

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


    emailInfo = {'emailSender': 'CELTS Admins'}

    emails = getParticipantEmails(1)
    email = emailHandler(app,emailInfo)
    emailSent = email.sendEmail(Message("this email is for testing",
                                       emails, # recipients
                                       "Yup, just testing, don't look any closer."),
                                       emails) # passed for sending individually
    print("Hello")

import pytest
from flask_mail import Message
from app.logic.emailHandler import *

@pytest.mark.integration
def test_getVolunteerEmails():

    programID = 1
    eventID = 1
    emailRecipients = "interested"

    volunteerEmails = getVolunteerEmails(programID, eventID, emailRecipients)
    assert "bryanta@berea.edu" in volunteerEmails

    # check for non existing programId
    programID = 40
    volunteerEmails = getVolunteerEmails(programID, eventID, emailRecipients)

    assert volunteerEmails == []

    # invalid eventID
    programID = 1
    eventID = -1
    emailRecipients = "eventParticipant"

    volunteerEmails = getVolunteerEmails(programID, eventID, emailRecipients)
    assert volunteerEmails == []

    # invalid recipients
    emailRecipients = 2
    volunteerEmails = getVolunteerEmails(programID, eventID, emailRecipients)
    assert volunteerEmails == None

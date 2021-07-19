import pytest
from app.logic.signinKiosk import sendkioskData
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_sendKioskDataKiosk():
    bnumber = "B00751864"
    eventid = 1
    signin = sendkioskData(bnumber, eventid)
    usersAttended = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == eventid)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "neillz" in listOfAttended

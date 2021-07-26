import pytest
from app.logic.signinKiosk import sendUserData
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_sendKioskDataKiosk():
    signin = sendUserData("B00751864", 1)
    usersAttended = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == eventid)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "neillz" in listOfAttended
    assert "ramsayb2" not in listOfAttended

@pytest.mark.integration
def test_correctAlreadySignedIn():
    user, signedin = sendUserData("B00751864", 2)
    assert signedin
    user, signedin = sendUserData("B00739736", 1)
    assert not signedin

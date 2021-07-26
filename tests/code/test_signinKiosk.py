import pytest
from app.logic.signinKiosk import sendUserData
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_sendKioskDataKiosk():
    bnumber = "B00751864"
    eventid = 1
    signin = sendUserData(bnumber, eventid)
    usersAttended = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == eventid)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "neillz" in listOfAttended
    assert "ramsayb2" not in listOfAttended

@pytest.mark.integration
def test_correctAlreadySignedIn():
    bnumber = "B00751864"  # user neillz
    eventid = 2
    user, signedin = sendUserData(bnumber, eventid)
    assert signedin
    bnumber = "B00739736" # user ayisie
    eventid = 1
    user, signedin = sendUserData(bnumber, eventid)
    assert not signedin

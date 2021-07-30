import pytest
from app.logic.signinKiosk import sendUserData
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_sendKioskDataKiosk():
    signin = sendUserData("B00751864", 1)
    usersAttended = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == 1)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "neillz" in listOfAttended
    assert "bryanta" not in listOfAttended

    (EventParticipant.update({EventParticipant.attended: False})
                     .where(EventParticipant.user == "neillz", EventParticipant.event == 1)).execute()


    signin = sendUserData("B00751864", 1)
    usersAttended = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == 1)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "bryanta" in listOfAttended

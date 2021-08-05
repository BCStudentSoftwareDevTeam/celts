import pytest
from app.logic.signinKiosk import sendUserData
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_sendKioskDataKiosk():
    signin = sendUserData("B00751864", 2, 1)
    usersAttended = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == 2)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "neillz" in listOfAttended
    assert "bryanta" not in listOfAttended

    (EventParticipant.update({EventParticipant.attended: False})
                     .where(EventParticipant.user == "neillz", EventParticipant.event == 1)).execute()


    signin = sendUserData("B00708826", 2, 1)
    usersAttended2 = EventParticipant.select().where(EventParticipant.attended, EventParticipant.event == 2)
    listOfAttended2 = [users.user.username for users in usersAttended2]

    assert "bryanta" in listOfAttended2

    deleteInstance = EventParticipant.get(EventParticipant.user == "bryanta")
    deleteInstance.delete_instance()

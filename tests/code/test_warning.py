import pytest
from peewee import DoesNotExist
from app.logic.trackAttendees import trainedParticipants

@pytest.mark.integration
def test_prereqParticipants():

    prlist = [1, 2]
    attendedPreq = prereqParticipant = trainedParticipants(1, prlist)

    assert "neillz" and "khatts" in attendedPreq

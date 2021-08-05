import pytest
from peewee import DoesNotExist
from app.logic.trackAttendees import trainedParticipants

@pytest.mark.integration
def test_prereqParticipants():
    attendedPreq = prereqParticipant = trainedParticipants(1)

    assert "neillz" and "khatts" in attendedPreq

import pytest
from peewee import DoesNotExist
from app.logic.trackAttendees import trainedParticipants

@pytest.mark.integration
def test_prereqParticipants():
    attendedPreq = trainedParticipants(1)
    assert "neillz" and "khatts" in attendedPreq

    #test for program with no prereq
    attendedPreq = trainedParticipants(4)
    assert attendedPreq == []

    #test for program that doesn't exist
    attendedPreq = trainedParticipants(500)
    assert attendedPreq == []

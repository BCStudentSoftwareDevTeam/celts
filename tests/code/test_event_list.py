import pytest
from peewee import DoesNotExist
from app.models.event import Event
from app.logic.events import getOneTimeEvents, getBonnerProgram, getTrainingProgram, getStudentLeadProgram

@pytest.mark.integration
def test_getOneTimeEvents():
    oneTimeEvents = getOneTimeEvents(1)

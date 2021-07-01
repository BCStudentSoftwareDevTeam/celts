import pytest
from peewee import DoesNotExist
from app.models.program import Program
from app.models.user import User
from app.models.event import Event
from app.controllers.events.viewAllEvents import groupingEvents

@pytest.mark.integration
def test_groupingEvents(user):
    events = groupingEvents()
    print(events)

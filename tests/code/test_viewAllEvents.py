import pytest
from peewee import DoesNotExist
from app.models.program import Program
from app.models.user import User
from app.models.event import Event
from app.models.term import Term
from app.controllers.events.viewAllEvents import groupingEvents

@pytest.mark.integration
def test_groupingEvents():

    term = Term.get_by_id(1)
    events = groupingEvents(term)
    print(events)

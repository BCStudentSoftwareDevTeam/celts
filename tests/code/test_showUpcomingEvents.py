import pytest
from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from peewee import DoesNotExist

@pytest.mark.integration
def test_getUpcomingEvents():
    user = "ramsayb2"
    upcomingEvent = getUpcomingEventsForUser(user)

    assert upcomingEvent

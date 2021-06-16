import pytest
from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from app.controllers.events.showUpcomingEvents import showUpcomingEvents
from peewee import DoesNotExist

@pytest.mark.integration
def test_show():
    user = "lamichhanes2"
    upcomingEvent = showUpcomingEvents(user)

    assert upcomingEvent

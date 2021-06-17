import pytest
from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from app.controllers.events.showUpcomingEvents import getUpcomingEventsForUser
from peewee import DoesNotExist

@pytest.mark.integration
def test_doesntExist():
    user = "hello"
    with pytest.raises(DoesNotExist):
        upcomingEvent = getUpcomingEventsForUser(user)

    user = 123546
    with pytest.raises(DoesNotExist):
        upcomingEvent = getUpcomingEventsForUser(user)

    user = " lamichhanes2"
    with pytest.raises(DoesNotExist):
        upcomingEvent = getUpcomingEventsForUser(user)

    user = "lamichhanes2 "
    with pytest.raises(DoesNotExist):
        upcomingEvent = getUpcomingEventsForUser(user)

@pytest.mark.integration
def test_show():
    user = "ramsayb2"
    upcomingEvent = getUpcomingEventsForUser(user)

    assert upcomingEvent

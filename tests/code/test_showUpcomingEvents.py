import pytest
from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from peewee import DoesNotExist

@pytest.mark.integration
def test_getsCorrectUpcomingEvent():

    user = "khatts"
    upcomingEvent = getUpcomingEventsForUser(user)

    assert "Empty Bowls Spring" == upcomingEvent[0].eventName

    with pytest.raises(AssertionError):
        assert "Potatoes" == upcomingEvent[0].eventName
        assert 156456 == upcomingEvent[0].eventName
        assert " Empty Bowls Spring" == upcomingEvent[0].eventName
        assert "Empty Bowls Spring " == upcomingEvent[0].eventName
        assert " Empty Bowls Spring " == upcomingEvent[0].eventName

@pytest.mark.integration
def test_userWithNoInterestedEvent():

    user = "bryanta"
    upcomingEvent = getUpcomingEventsForUser(user)

    with pytest.raises(IndexError):
        assert "Empty Bowls Spring" == upcomingEvent[0].eventName
        assert 132154 == upcomingEvent[15].eventName


@pytest.mark.integration
def test_getUpcomingEvents():
    user = "ramsayb2"
    upcomingEvent = getUpcomingEventsForUser(user)

    assert len(upcomingEvent) > 0

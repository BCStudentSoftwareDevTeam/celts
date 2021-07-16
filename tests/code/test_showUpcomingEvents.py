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

    user = "ramsayb2"
    upcomingEvent = getUpcomingEventsForUser(user)
    assert "Berea Buddies" == upcomingEvent[0].program.programName


@pytest.mark.integration
def test_userWithNoInterestedEvent():

    user ="asdfasd" #invalid user
    upcomingEvent = getUpcomingEventsForUser(user)
    assert len(upcomingEvent) == 0

    user = "bryanta" #no interest selected
    upcomingEvent = getUpcomingEventsForUser(user)
    assert len(upcomingEvent) == 0

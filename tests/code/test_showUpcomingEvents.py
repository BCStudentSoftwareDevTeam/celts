import pytest
from datetime import datetime
from app.models import mainDB
from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from peewee import DoesNotExist

@pytest.mark.integration
def test_getsCorrectUpcomingEvent():

    testDate = datetime.strptime("2021-08-01 5:00","%Y-%m-%d %H:%M")

    user = "khatts"
    events = getUpcomingEventsForUser(user, asOf=testDate)
    assert len(events) == 3
    assert "Empty Bowls Spring" == events[0].eventName

    user = "ramsayb2"
    events = getUpcomingEventsForUser(user, asOf=testDate)
    assert len(events) == 5
    assert "Making Bowls" == events[0].eventName

@pytest.mark.integration
def test_userWithNoInterestedEvent():

    user ="asdfasd" #invalid user
    events = getUpcomingEventsForUser(user)
    assert len(events) == 0

    user = "bryanta" #no interest selected
    events = getUpcomingEventsForUser(user)
    assert len(events) == 0

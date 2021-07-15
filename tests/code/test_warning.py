import pytest
from peewee import DoesNotExist
from app.logic.trackVolunteerHours import prereqParticipants
from app.controllers.admin.routes import trackVolunteerHoursPage
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_prereqParticipants():

    prlist = [1, 2]
    prereqParticipant = prereqParticipants(1, prlist)
    eventPreqDataList = []

    eventPreqDataList = [participant.user.username for participant in (EventParticipant.select().where(EventParticipant.event.in_(prlist)))]
    attendedPreq = list(dict.fromkeys(filter(lambda user: eventPreqDataList.count(user) == len(prlist), eventPreqDataList)))

    assert "neillz" and "khatts" in attendedPreq

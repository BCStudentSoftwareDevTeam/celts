import pytest
from datetime import date, datetime, timedelta

from app.models import mainDB
from app.models.event import Event
from app.logic.events import getTomorrowsEvents
from app.scripts.sendEventReminderEmails import sendAutomatedEmail


@pytest.mark.integration
@pytest.mark.skip(reason="Authentication issues")
def test_sendAutomatedEmail():
    with mainDB.atomic() as transaction:
        tomorrow = date.today() + timedelta(days=1)
        emailsSent = sendAutomatedEmail([])
        assert emailsSent == 0  # if no events are found, should return 0
        newEvent = Event.create(
            name="Test event",
            term=2,
            description="This Event is Created to be Deleted.",
            timeStart="6:00 pm",
            timeEnd="9:00 pm",
            location="No Where",
            isRsvpRequired=0,
            isTraining=0,
            isService=0,
            startDate=tomorrow,
            endDate="2022-12-19",
            recurringId=0,
        )
        tomorrowEvents = getTomorrowsEvents()
        emailsSent = sendAutomatedEmail(tomorrowEvents)
        assert emailsSent == 1
        assert len(tomorrowEvents) == 1
        newEvent = Event.create(
            name="Testing event",
            term=2,
            description="This Event is Created to be Deleted.",
            timeStart="6:00 pm",
            timeEnd="9:00 pm",
            location="No Where",
            isRsvpRequired=0,
            isTraining=0,
            isService=0,
            startDate=tomorrow,
            endDate="2022-12-19",
            recurringId=0,
        )
        tomorrowEvents = getTomorrowsEvents()
        emailsSent = sendAutomatedEmail(tomorrowEvents)
        assert emailsSent == 2
        assert len(tomorrowEvents) == 2
        transaction.rollback()

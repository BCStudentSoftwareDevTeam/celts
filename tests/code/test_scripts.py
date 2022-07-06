import pytest
from dateutil import parser
from datetime import date, datetime, timedelta

from app.models.user import User
from app.models import mainDB
from app.models.event import Event
from app.models.program import Program
from app.logic.events import saveEventToDb
from app.scripts.sendEventReminderEmails import checkForEvents, sendAutomatedEmail

@pytest.mark.integration
def test_checkForEvents():
    with mainDB.atomic() as transaction:
        tomorrow = date.today() + timedelta(days=1)
        newEvent = Event.create(name = "Test event",
                      term = 2,
                      description= "This Event is Created to be Deleted.",
                      timeStart= "6:00 pm",
                      timeEnd= "9:00 pm",
                      location = "No Where",
                      isRsvpRequired = 0,
                      isTraining = 0,
                      isService = 0,
                      startDate=  tomorrow,
                      endDate= "2022-12-19",
                      recurringId = 0)
        tomorrowEvents = checkForEvents()
        emailsSent = sendAutomatedEmail(tomorrowEvents)
        assert emailsSent == 1
        assert len(tomorrowEvents) == 1
        newEvent = Event.create(name = "Testing event",
                      term = 2,
                      description= "This Event is Created to be Deleted.",
                      timeStart= "6:00 pm",
                      timeEnd= "9:00 pm",
                      location = "No Where",
                      isRsvpRequired = 0,
                      isTraining = 0,
                      isService = 0,
                      startDate=  tomorrow,
                      endDate= "2022-12-19",
                      recurringId = 0)
        tomorrowEvents = checkForEvents()
        emailsSent = sendAutomatedEmail(tomorrowEvents)
        assert emailsSent == 2
        assert len(tomorrowEvents) == 2
        transaction.rollback()

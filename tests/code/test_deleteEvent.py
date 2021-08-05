import pytest
from app.controllers.admin.deleteEvent import deleteEvent
from app.models.event import Event

@pytest.mark.integration
def test_deleteEvent():

    testingEvent = Event.create(eventName = "Testing delete event",
                                  term = 2,
                                  description= "This Event is Created to be Deleted.",
                                  timeStart= "6:00 pm",
                                  timeEnd= "9:00 pm",
                                  location = "No Where",
                                  isRecurring = 0,
                                  isRsvpRequired = 0,
                                  isTraining = 0,
                                  isService = 0,
                                  startDate= "2021 12 12",
                                  endDate= "2022 6 12")

    testingEvent = Event.get(Event.eventName == "Testing delete event")

    program = 1
    eventId = testingEvent.id
    deletingEvent = deleteEvent(program, eventId)
    assert Event.get_or_none(Event.id == eventId) is None

    deletingEvent = deleteEvent(program, eventId)
    assert Event.get_or_none(Event.id == eventId) is None

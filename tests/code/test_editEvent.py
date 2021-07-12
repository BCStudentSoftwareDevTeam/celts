import pytest
from app.logic.adminNewEvent import eventEdit
from app.models.event import Event
from datetime import *


@pytest.mark.integration
def test_beforeEdit():
    eventId = 2
    beforeEdit = Event.get_by_id(eventId)

    assert beforeEdit.eventName == "Berea Buddies"

@pytest.mark.integration
def test_afterEdit():
    eventFunction: editEvent(newEventData)
    eventId = 2
    eventData = {
                    "id": eventId,
                    "program": 1,
                    "term": 1,
                    "eventName": "Berea Buddies",
                    "description": "This is a Test",
                    "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
                    "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
                    "location": "House",
                    "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
                    "endDate": datetime.strptime("2022 6 12","%Y %m %d")
                }
    eventEntry = Event.update(**eventData).where(Event.id == eventId).execute()
    afterEdit = Event.get_by_id(eventId)

    assert afterEdit.description == "This is a Test"

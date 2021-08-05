import pytest
from app.models.user import User
from app.logic.adminNewEvent import eventEdit
from app.controllers.admin.createEvents import *
from app.models.event import Event
from datetime import *


@pytest.mark.integration
def test_beforeEdit():
    eventId = 4
    beforeEdit = Event.get_by_id(eventId)

    assert beforeEdit.eventName == "First Meetup"

@pytest.mark.integration
def test_afterEdit():
    newEventData = {
                    "eventId": 4,
                    "program": 1,
                    "eventTerm": 1,
                    "eventName": "First Meetup",
                    "eventDescription": "This is a Test",
                    "eventStartTime": datetime.strptime("6:00 pm", "%I:%M %p"),
                    "eventEndTime": datetime.strptime("9:00 pm", "%I:%M %p"),
                    "eventLocation": "House",
                    'eventIsRecurring': True,
                    'eventIsTraining': True,
                    'eventRSVP': False,
                    'eventServiceHours': 5,
                    "eventStartDate": "2021 12 12",
                    "eventEndDate": "2022 6 12"
                }
    newEventData.update(valid=True, eventFacilitator=User.get(User.username == 'ramsayb2'))
    eventFunction = eventEdit(newEventData)
    afterEdit = Event.get_by_id(newEventData['eventId'])
    assert afterEdit.description == "This is a Test"
    newEventData = {
                    "eventId": 4,
                    "program": 1,
                    "eventTerm": 1,
                    "eventName": "First Meetup",
                    "eventDescription": "Berea Buddies First Meetup",
                    "eventStartTime": datetime.strptime("6:00 pm", "%I:%M %p"),
                    "eventEndTime": datetime.strptime("9:00 pm", "%I:%M %p"),
                    "eventLocation": "House",
                    'eventIsRecurring': True,
                    'eventIsTraining': True,
                    'eventRSVP': False,
                    'eventServiceHours': 5,
                    "eventStartDate": "2021 12 12",
                    "eventEndDate": "2022 6 12"
                }
    newEventData.update(valid=True, eventFacilitator=User.get(User.username == 'ramsayb2'))
    eventFunction = eventEdit(newEventData)
    afterEdit = Event.get_by_id(newEventData['eventId'])

    assert afterEdit.description == "Berea Buddies First Meetup"

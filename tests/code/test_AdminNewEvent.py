import pytest
from app.logic.adminNewEvent import manageNewEventData, createEvent

@pytest.mark.integration
def test_manageNewEventData():
    eventData = {'eventRequiredForProgram':1,'eventRSVP':2, 'eventServiceHours':3 }

    newData = manageNewEventData(eventData)


    pass




def test_createEvent():
    pass

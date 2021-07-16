import pytest
from app.logic.adminNewEvent import calculateRecurringEventFrequency
import json

@pytest.mark.integration
def test_calculateRecurringEventFrequency():

    eventInfo = {'eventName':"testEvent",
                 'eventStartDate':"02-22-2023",
                 'eventEndDate': "03-9-2023"}

    returnedEvents = json.loads(calculateRecurringEventFrequency(eventInfo))
    #test correct response
    assert returnedEvents[0] == {'eventName': 'testEvent Week 1', 'Date': '02-22-2023', 'week': 1}
    assert returnedEvents[1] == {'eventName': 'testEvent Week 2', 'Date': '03-01-2023', 'week': 2}
    assert returnedEvents[2] == {'eventName': 'testEvent Week 3', 'Date': '03-08-2023', 'week': 3}

    #test incorrect value
    eventInfo["eventStartDate"] = "hello"
    with pytest.raises(ValueError):
        returnedEvents = json.loads(calculateRecurringEventFrequency(eventInfo))

    #test incorect date format
    eventInfo["eventStartDate"] = "02/22/2023"
    with pytest.raises(ValueError):
        returnedEvents = json.loads(calculateRecurringEventFrequency(eventInfo))

    #test incorrect date
    eventInfo["eventStartDate"] = "02-29-2023"
    with pytest.raises(ValueError):
        returnedEvents = json.loads(calculateRecurringEventFrequency(eventInfo))

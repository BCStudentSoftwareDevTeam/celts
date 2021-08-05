import pytest
from app.logic.adminNewEvent import calculateRecurringEventFrequency

@pytest.mark.integration
def test_calculateRecurringEventFrequency():

    eventInfo = {'eventName':"testEvent",
                 'eventStartDate':"02-22-2023",
                 'eventEndDate': "03-9-2023"}

    returnedEvents = calculateRecurringEventFrequency(eventInfo)
    #test correct response
    assert returnedEvents[0] == {'eventName': 'testEvent Week 1', 'date': '02-22-2023', 'week': 1}
    assert returnedEvents[1] == {'eventName': 'testEvent Week 2', 'date': '03-01-2023', 'week': 2}
    assert returnedEvents[2] == {'eventName': 'testEvent Week 3', 'date': '03-08-2023', 'week': 3}

    #test incorrect value
    eventInfo["eventStartDate"] = "hello"
    with pytest.raises(ValueError):
        returnedEvents = calculateRecurringEventFrequency(eventInfo)

    #test incorect date format
    eventInfo["eventStartDate"] = "02/22/2023"
    with pytest.raises(ValueError):
        returnedEvents = calculateRecurringEventFrequency(eventInfo)

    #test incorrect date
    eventInfo["eventStartDate"] = "02-29-2023"
    with pytest.raises(ValueError):
        returnedEvents = calculateRecurringEventFrequency(eventInfo)

import pytest
from app.logic.adminNewEvent import calculateRecurringEventFrequency

@pytest.mark.integration
def test_calculateRecurringEventFrequency():

    eventInfo = {'eventName':"testEvent",
                 'eventStartDate':"02/22/2023",
                 'eventEndDate': "03/9/2023",
                 "eventFrequency":"weekly"}

    calculateRecurringEventFrequency(eventInfo)
    print("======================================================")

    eventInfo = {'eventName':"testEvent",
                 'eventStartDate':"02/22/2023",
                 'eventEndDate': "03/9/2023",
                 "eventFrequency":"daily"}

    calculateRecurringEventFrequency(eventInfo)

    print("======================================================")

    eventInfo = {'eventName':"testEvent",
                 'eventStartDate':"02/22/2023",
                 'eventEndDate': "09/9/2023",
                 "eventFrequency":"monthly"}

    calculateRecurringEventFrequency(eventInfo)

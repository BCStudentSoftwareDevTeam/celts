import pytest

from app.logic.validateNewEvent import validateNewEventData
from datetime import datetime

@pytest.mark.integration
def test_correctValidateNewEventData():

    validateEventData =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                          'eventIsTraining':True, 'eventIsRecurring':False, 'eventStartDate': '1999-12-12',
                          'eventEndDate':'2022-06-12', 'programId':1, 'eventLocation':"a big room",
                          'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                          'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)

    # assert validNewEvent == True
    assert eventErrorMessage == "All inputs are valid."


@pytest.mark.integration
def test_wrongValidateNewEventData():

    validateEventData =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                          'eventIsTraining':True, 'eventIsRecurring':False, 'eventStartDate': '2021-12-12',
                          'eventEndDate': '2021-06-12', 'programId':1, 'eventLocation':"a big room",
                          'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                          'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)

    assert validNewEvent == False
    assert eventErrorMessage == "Event start date is after event end date"

    # testing event starts after it ends.
    validateEventData["eventStartDate"] = '2021-06-12'
    validateEventData["eventStartTime"] =  '21:39'

    validateNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)

    assert validNewEvent == False
    assert eventErrorMessage == "Event start time is after event end time"


    # testing same event already exists
    validateEventData["eventRequiredForProgram"] = True
    validateEventData["eventStartDate"] = '2021-12-12'
    validateEventData['eventEndDate'] = '2022-06-12'

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)
    assert validNewEvent == False
    assert eventErrorMessage == "This event already exists"

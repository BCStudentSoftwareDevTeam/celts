import pytest

from app.logic.validateNewEvent import validateNewEventData
from datetime import datetime

@pytest.mark.integration
def test_correctValidateNewEventData():

    validateEventData =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                          'eventIsTraining':True, 'eventIsRecurring':False, 'eventStartDate': datetime.strptime('1999-12-12', '%Y-%m-%d'),
                          'eventEndDate':datetime.strptime('2022-06-12', '%Y-%m-%d'), 'programId':1, 'eventLocation':"a big room",
                          'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                          'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)

    # assert validNewEvent == True
    assert eventErrorMessage == "All inputs are valid."


@pytest.mark.integration
def test_wrongValidateNewEventData():

    validateEventData =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                          'eventIsTraining':True, 'eventIsRecurring':False, 'eventStartDate': datetime.strptime('2021-12-12', '%Y-%m-%d'),
                          'eventEndDate':datetime.strptime('2021-06-12', '%Y-%m-%d'), 'programId':1, 'eventLocation':"a big room",
                          'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                          'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)

    assert validNewEvent == False
    assert eventErrorMessage == "Event start date is after event end date"

    # testing event starts after it ends.
    validateEventData["eventStartDate"] = datetime.strptime('2021-06-12', '%Y-%m-%d')
    validateEventData["eventStartTime"] =  '21:39'

    validateNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)

    assert validNewEvent == False
    assert eventErrorMessage == "Event start time is after event end time"


    # testing same event already exists
    validateEventData["eventRequiredForProgram"] = True
    validateEventData["eventStartDate"] = datetime.strptime("2021-12-12", '%Y-%m-%d')
    validateEventData['eventEndDate'] = datetime.strptime('2022-06-12', '%Y-%m-%d')

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)
    assert validNewEvent == False
    assert eventErrorMessage == "This event already exists"

import pytest
from app.logic.validateNewEvent import validateNewEventData

@pytest.mark.integration
def test_correctValidateNewEventData():

    validateEventData = {'eventEndDate': '2021-07-03', 'eventStartDate':'2021-07-02',
                         'eventStartTime': '10:33', 'eventEndTime':'10:35',
                         'eventIsTraining':'on', 'eventRequiredForProgram':True,
                         'eventName':'Berea Buddies', 'eventDescription':'Berea Buddies Training'}
    validateNewEvent = validateNewEventData(validateEventData)

    # check return type
    assert type(validateNewEvent) == type(())

    assert validateNewEvent[0] == True
    assert validateNewEvent[1] == "All inputs are valid."


@pytest.mark.integration
def test_wrongValidateNewEventData():

    validateEventData = {'eventEndDate': '2021-07-03', 'eventStartDate':'2021-07-05',
                         'eventStartTime': '10:33', 'eventEndTime':'10:35',
                         'eventIsTraining':'on', 'eventRequiredForProgram':True,
                         'eventName':'Berea Buddies', 'eventDescription':'Berea Buddies Training'}

    validateNewEvent = validateNewEventData(validateEventData)

    assert validateNewEvent[0] == False
    assert validateNewEvent[1] == "Event start date is after event end date"

    # testing event starts after it ends.
    validateEventData["eventStartDate"] = '2021-07-03'
    validateEventData["eventStartTime"] =  '10:39'

    validateNewEvent = validateNewEventData(validateEventData)

    assert validateNewEvent[0] == False
    assert validateNewEvent[1] == "Event start time is after event end time"

    # Testing for Event Training and Event is Required Validation
    validateEventData["eventStartTime"] = '10:33'
    validateEventData["eventRequiredForProgram"] = False

    validateNewEvent = validateNewEventData(validateEventData)

    assert validateNewEvent[0] == False
    assert validateNewEvent[1] == "A training event must be required for the program."

    # testing same event already exists
    validateEventData["eventRequiredForProgram"] = True
    validateEventData["eventStartDate"] = "2021-06-15"

    validateNewEvent = validateNewEventData(validateEventData)
    assert validateNewEvent[0] == False
    assert validateNewEvent[1] == "This event already exists"

import pytest
from app.logic.adminNewEvent import manageNewEventData, createEvent

@pytest.mark.integration
def test_manageNewEventData():

    # test that there is a return
    assert manageNewEventData({})

    # tets for return type
    assert type(manageNewEventData({}))== type({})

    # test for no keys
    eventData = {}
    newData = manageNewEventData(eventData)
    assert newData['eventRequiredForProgram'] == False
    assert newData['eventRSVP'] == False
    assert newData['eventServiceHours'] == False
    assert newData['eventIsTraining'] == False

    #test for one missing key
    eventData = {'eventRequiredForProgram':'on','eventRSVP':'', 'eventServiceHours':True }
    newData = manageNewEventData(eventData)

    assert newData['eventIsTraining'] == False
    with pytest.raises(AssertionError):
        assert newData['eventRSVP'] == 'gfg'
        assert newData['eventServiceHours'] == False
        assert newData['eventRequiredForProgram'] == 1

    # test for dict with values
    eventData = {'eventRequiredForProgram':1,'eventRSVP':2, 'eventServiceHours':3, 'eventIsTraining':4}
    newData = manageNewEventData(eventData)

    assert newData['eventRequiredForProgram'] == 1
    assert newData['eventRSVP'] == 2
    assert newData['eventServiceHours'] == 3
    assert newData['eventIsTraining'] == 4




def test_createEvent():
    pass

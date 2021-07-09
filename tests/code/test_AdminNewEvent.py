import pytest
from app.logic.adminNewEvent import setValueForUncheckedBox, createNewEvent

@pytest.mark.integration
def test_setValueForUncheckedBox():

    # test that there is a return
    assert setValueForUncheckedBox({})

    # tets for return type
    assert type(setValueForUncheckedBox({}))== type({})

    # test for no keys
    eventData = {}
    newData = setValueForUncheckedBox(eventData)
    assert newData['eventRequiredForProgram'] == False
    assert newData['eventRSVP'] == False
    assert newData['eventServiceHours'] == False
    assert newData['eventIsTraining'] == False

    #test for one missing key
    eventData = {'eventRequiredForProgram':'on','eventRSVP':'', 'eventServiceHours':True }
    newData = setValueForUncheckedBox(eventData)

    assert newData['eventIsTraining'] == False  #the value of newData['eventIsTraining'] is false

    with pytest.raises(AssertionError):
        assert newData['eventRSVP'] == 'gfg'
        assert newData['eventServiceHours'] == False
        assert newData['eventRequiredForProgram'] == 1

    # test for dict with values
    eventData = {'eventRequiredForProgram':1,'eventRSVP':2, 'eventServiceHours':3, 'eventIsTraining':4}
    newData = setValueForUncheckedBox(eventData)

    assert newData['eventRequiredForProgram'] == 1
    assert newData['eventRSVP'] == 2
    assert newData['eventServiceHours'] == 3
    assert newData['eventIsTraining'] == 4




def test_createNewEvent():
    pass

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

    # check that the setValueForUncheckedBox does not change existing keys
    assert newData['eventRSVP'] == ''
    assert newData['eventServiceHours'] == True
    assert newData['eventRequiredForProgram'] == 'on'

    




def test_createNewEvent():
    pass

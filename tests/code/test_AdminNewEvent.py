import pytest
from app.logic.adminNewEvent import setValueForUncheckedBox, createNewEvent
from peewee import OperationalError, IntegrityError


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


@pytest.mark.integration
def test_createNewEvent():

    eventInfo =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                  'eventIsTraining':True, 'eventIsRecurring':False, 'eventStartDate': '2021-12-12',
                   'eventEndDate':'2022-06-12', 'programId':1, 'eventLocation':"a big room",
                   'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                   'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}
    alertMessage = createNewEvent(eventInfo)
    assert alertMessage == "Event successfully created!"


    # FIXME: the test below don't work as expected ... is there a fix or should it be deleated?
    # #test Date field startDate
    # # eventInfo["eventStartDate"] = "Hi, how are you?"
    # with pytest.raises(OperationalError):
    #     alertMessage = createNewEvent(eventInfo)
    #
    # # test foregin key username
    # # eventInfo["eventStartDate"] = '2021-12-12'
    # # eventInfo["eventFacilitator"] = "jarjug"
    # # with pytest.raises(IntegrityError):
    # #     alertMessage = createNewEvent(eventInfo)
    #
    #
    # #tests boolean RSVP
    # # eventInfo["eventFacilitator"] = "ramsayb2"
    # # eventInfo["eventRSVP"] = [2,3,4]
    # # with pytest.raises(OperationalError):
    #     # alertMessage = createNewEvent(eventInfo)

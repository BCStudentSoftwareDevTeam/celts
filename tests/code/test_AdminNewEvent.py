import pytest
from app.logic.adminNewEvent import setValueForUncheckedBox, createNewEvent
from peewee import OperationalError, IntegrityError
from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator


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

    # if valid is not added to the dict
    with pytest.raises(KeyError):
        createNewEvent(eventInfo)

    # if 'valid' is not True
    eventInfo['valid'] = False
    with pytest.raises(Exception):
        createNewEvent(eventInfo)

    #test that the event and facilitators are added successfully
    eventInfo['valid'] = True
    createdEvent = createNewEvent(eventInfo)
    assert createdEvent.singleProgram.id == 1

    createdEventFacilitator = Facilitator.get(user=eventInfo['eventFacilitator'], event=createdEvent)
    assert createdEventFacilitator # kind of redundant, as the previous line will throw an exception

    createdEventFacilitator.delete_instance()
    ProgramEvent.delete().where(ProgramEvent.event_id == createdEvent.id).execute()
    Event.delete().where(Event.id == createdEvent.id).execute()

    # test bad username for facilitator (user does not exist)
    eventInfo["eventFacilitator"] = "jarjug"
    with pytest.raises(IntegrityError):
        createNewEvent(eventInfo)


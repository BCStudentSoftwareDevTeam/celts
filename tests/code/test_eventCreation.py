import pytest
from datetime import datetime
from peewee import OperationalError, IntegrityError

from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator
from app.logic.eventCreation import validateNewEventData, setValueForUncheckedBox, createNewEvent, calculateRecurringEventFrequency

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

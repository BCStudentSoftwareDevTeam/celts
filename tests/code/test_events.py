import pytest
from peewee import DoesNotExist, OperationalError, IntegrityError
from datetime import datetime

from app.models.event import Event
from app.models.user import User
from app.models.eventTemplate import EventTemplate
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.models.facilitator import Facilitator
from app.models.interest import Interest
from app.logic.events import attemptSaveEvent, saveEventToDb, getEvents, deleteEvent, groupEventsByCategory, groupEventsByProgram
from app.logic.events import getAllFacilitators, getUpcomingEventsForUser
from app.logic.eventCreation import validateNewEventData, setValueForUncheckedBox, calculateRecurringEventFrequency


@pytest.mark.integration
def test_event_model():
    # single program
    event = Event.get_by_id(12)
    assert event.singleProgram == Program.get_by_id(3)

    # no program
    event = Event.get_by_id(13)
    assert event.singleProgram == None
    assert event.noProgram

    # multi program
    event = Event.get_by_id(14)
    assert event.singleProgram == None
    assert not event.noProgram


@pytest.mark.integration
def test_getAllEvents():
    # No program is given, get all events
    events = getEvents()


    assert len(events) > 0


    assert events[0].description == "Empty Bowls Spring 2021"
    assert events[1].description == "Berea Buddies Training"
    assert events[2].description == "Adopt A Grandparent"

@pytest.mark.integration
def test_getEventsWithProgram():
    # Single program
    events = getEvents(program_id=2)


    assert len(events) > 0


    assert events[0].description == "Berea Buddies First Meetup"

@pytest.mark.integration
def test_getEventsInvalidProgram():
    # Invalid program
    with pytest.raises(DoesNotExist):
        getEvents(program_id= "asdf")

@pytest.mark.integration
def test_eventTemplate_model():

    template = EventTemplate(name="test", templateJSON='{"first entry":["number one", "number two"]}')
    assert template.templateData == {"first entry": ["number one", "number two"]}

    template.templateData = ["just", "an", "array"]
    template.save()

    template = EventTemplate.get(name="test")
    assert template.templateData == ["just", "an", "array"]

    template.delete_instance()

@pytest.mark.integration
def test_eventTemplate_fetch():

    template = EventTemplate(name="test2")
    template.templateData = {
                "first entry": "number one",
                "second entry": "number two",
                "fourth entry": "number four"
            }
    assert "number one" == template.fetch("first entry")
    assert "number one" == template.fetch("first entry", "1")

    assert None == template.fetch("third entry")
    assert "3" == template.fetch("third entry", "3")

    template.save()
    template.delete_instance()

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


    # testing same event already exists if no event id
    validateEventData["eventRequiredForProgram"] = True
    validateEventData["eventStartDate"] = '2021-10-12'
    validateEventData['eventEndDate'] = '2022-06-12'

    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)
    assert validNewEvent == False
    assert eventErrorMessage == "This event already exists"

    # If we provide an event id, don't check for existence
    validateEventData['eventId'] = 5
    validNewEvent, eventErrorMessage, eventData = validateNewEventData(validateEventData)
    assert validNewEvent == True

@pytest.mark.integration
def test_attemptSaveEvent():
    pass

@pytest.mark.integration
def test_saveEventToDb_create():

    eventInfo =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                  'eventIsTraining':True, 'eventIsRecurring':False, 'eventStartDate': '2021-12-12',
                   'eventEndDate':'2022-06-12', 'eventLocation':"a big room", 
                   'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                   'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}
    eventInfo['program'] = Program.get_by_id(1)

    # if valid is not added to the dict
    with pytest.raises(Exception):
        saveEventToDb(eventInfo)

    # if 'valid' is not True
    eventInfo['valid'] = False
    with pytest.raises(Exception):
        saveEventToDb(eventInfo)

    #test that the event and facilitators are added successfully
    eventInfo['valid'] = True
    createdEvents = saveEventToDb(eventInfo)
    assert len(createdEvents) == 1
    assert createdEvents[0].singleProgram.id == 1

    createdEventFacilitator = Facilitator.get(user=eventInfo['eventFacilitator'], event=createdEvents[0])
    assert createdEventFacilitator # kind of redundant, as the previous line will throw an exception

    createdEventFacilitator.delete_instance()
    ProgramEvent.delete().where(ProgramEvent.event_id == createdEvents[0].id).execute()
    Event.delete().where(Event.id == createdEvents[0].id).execute()

    # test bad username for facilitator (user does not exist)
    eventInfo["eventFacilitator"] = "jarjug"
    with pytest.raises(IntegrityError):
        saveEventToDb(eventInfo)

@pytest.mark.integration
def test_saveEventToDb_recurring():
    eventInfo =  {'eventRequiredForProgram':True,'eventRSVP':False, 'eventServiceHours':False,
                  'eventIsTraining':True, 'eventIsRecurring': 'on', 'eventStartDate': '12-12-2021',
                   'eventEndDate':'01-18-2022', 'eventLocation':"this is only a test",
                   'eventEndTime':'21:00', 'eventStartTime':'18:00', 'eventDescription':"Empty Bowls Spring 2021",
                   'eventName':'Empty Bowls Spring','eventTerm':1,'eventFacilitator':"ramsayb2"}
    eventInfo['valid'] = True
    eventInfo['program'] = Program.get_by_id(1)
    createdEvents = saveEventToDb(eventInfo)
    assert len(createdEvents) == 6

    for event in Event.select().where(Event.location == "this is only a test"):
        event.delete_instance(recursive = True)


@pytest.mark.integration
def test_saveEventToDb_update():
    eventId = 4
    beforeUpdate = Event.get_by_id(eventId)
    assert beforeUpdate.name == "First Meetup"

    newEventData = {
                    "eventId": 4,
                    "program": 1,
                    "eventTerm": 1,
                    "eventName": "First Meetup",
                    "eventDescription": "This is a Test",
                    "eventStartTime": datetime.strptime("6:00 pm", "%I:%M %p"),
                    "eventEndTime": datetime.strptime("9:00 pm", "%I:%M %p"),
                    "eventLocation": "House",
                    'eventIsRecurring': True,
                    'eventIsTraining': True,
                    'eventRSVP': False,
                    'eventServiceHours': 5,
                    "eventStartDate": "2021 12 12",
                    "eventEndDate": "2022 6 12",
                    "eventFacilitator": User.get(User.username == 'ramsayb2'),
                    "valid": True
                }
    eventFunction = saveEventToDb(newEventData)
    afterUpdate = Event.get_by_id(newEventData['eventId'])
    assert afterUpdate.description == "This is a Test"

    newEventData = {
                    "eventId": 4,
                    "program": 1,
                    "eventTerm": 1,
                    "eventName": "First Meetup",
                    "eventDescription": "Berea Buddies First Meetup",
                    "eventStartTime": datetime.strptime("6:00 pm", "%I:%M %p"),
                    "eventEndTime": datetime.strptime("9:00 pm", "%I:%M %p"),
                    "eventLocation": "House",
                    'eventIsRecurring': True,
                    'eventIsTraining': True,
                    'eventRSVP': False,
                    'eventServiceHours': 5,
                    "eventStartDate": "2021 12 12",
                    "eventEndDate": "2022 6 12",
                    "eventFacilitator": User.get(User.username == 'ramsayb2'),
                    "valid": True
                }
    eventFunction = saveEventToDb(newEventData)
    afterUpdate = Event.get_by_id(newEventData['eventId'])

    assert afterUpdate.description == "Berea Buddies First Meetup"

@pytest.mark.integration
def test_calculateRecurringEventFrequency():

    eventInfo = {'eventName':"testEvent",
                 'eventStartDate':"02-22-2023",
                 'eventEndDate': "03-9-2023"}

    returnedEvents = calculateRecurringEventFrequency(eventInfo)
    #test correct response
    assert returnedEvents[0] == {'name': 'testEvent Week 1', 'date': '02-22-2023', 'week': 1}
    assert returnedEvents[1] == {'name': 'testEvent Week 2', 'date': '03-01-2023', 'week': 2}
    assert returnedEvents[2] == {'name': 'testEvent Week 3', 'date': '03-08-2023', 'week': 3}

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
@pytest.mark.integration
def test_deleteEvent():

    testingEvent = Event.create(name = "Testing delete event",
                                  term = 2,
                                  description= "This Event is Created to be Deleted.",
                                  timeStart= "6:00 pm",
                                  timeEnd= "9:00 pm",
                                  location = "No Where",
                                  isRecurring = 0,
                                  isRsvpRequired = 0,
                                  isTraining = 0,
                                  isService = 0,
                                  startDate= "2021 12 12",
                                  endDate= "2022 6 12")

    testingEvent = Event.get(Event.name == "Testing delete event")

    eventId = testingEvent.id
    deletingEvent = deleteEvent(eventId)
    assert Event.get_or_none(Event.id == eventId) is None

    deletingEvent = deleteEvent(eventId)
    assert Event.get_or_none(Event.id == eventId) is None

@pytest.mark.integration
def test_termDoesNotExist():
    with pytest.raises(DoesNotExist):
        groupedEvents = groupEventsByCategory(7)

    with pytest.raises(DoesNotExist):
        groupedEvents2 = groupEventsByCategory("khatts")

    with pytest.raises(DoesNotExist):
        groupedEvents3 = groupEventsByCategory("")

@pytest.mark.integration
def test_groupEventsByProgram():
    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == 1))
    assert groupEventsByProgram(studentLedEvents) == {Program.get_by_id(1): [Event.get_by_id(1), Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]}

    trainingEvents = (Event.select(Event, Program.id.alias("program_id"))
                           .join(ProgramEvent)
                           .join(Program)
                           .where(Event.isTraining,
                                  Event.term == 1))
    assert groupEventsByProgram(trainingEvents) == {Program.get_by_id(1): [Event.get_by_id(1) , Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]}

    bonnerScholarsEvents = (Event.select(Event, Program.id.alias("program_id"))
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == 1))
    assert groupEventsByProgram(bonnerScholarsEvents) == {}

    oneTimeEvents = (Event.select(Event, Program.id.alias("program_id"))
                          .join(ProgramEvent)
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False,
                                 Event.term == 1))
    assert groupEventsByProgram(oneTimeEvents) == {}


@pytest.mark.integration
def test_groupEventsByCategory():
    groupedEventsByCategory = groupEventsByCategory(1)
    assert groupedEventsByCategory == {"Student Led Events" : {Program.get_by_id(1): [Event.get_by_id(1), Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]},
                         "Trainings" : {Program.get_by_id(1): [Event.get_by_id(1) , Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]} ,
                         "Bonner Scholars" : {} ,
                         "One Time Events" : {} }

    assert groupedEventsByCategory

@pytest.mark.integration
def test_getAllFacilitators():
    userFacilitator = getAllFacilitators()

    assert len(userFacilitator) >= 1
    assert userFacilitator[1].username == 'lamichhanes2'
    assert userFacilitator[1].isFaculty == True
    assert userFacilitator[0].username == "khatts"
    assert userFacilitator[0].isFaculty == False

@pytest.mark.integration
def test_getsCorrectUpcomingEvent():

    testDate = datetime.strptime("2021-08-01 5:00","%Y-%m-%d %H:%M")

    user = "khatts"
    events = getUpcomingEventsForUser(user, asOf=testDate)
    assert len(events) == 3
    assert "Empty Bowls Spring" == events[0].name

    user = "ramsayb2"
    events = getUpcomingEventsForUser(user, asOf=testDate)
    assert len(events) == 5
    assert "Making Bowls" == events[0].name


@pytest.mark.integration
def test_userWithNoInterestedEvent():

    user ="asdfasd" #invalid user
    events = getUpcomingEventsForUser(user)
    assert len(events) == 0

    user = "ayisie" #no interest selected
    events = getUpcomingEventsForUser(user)
    assert len(events) == 0

import pytest
from peewee import DoesNotExist
from datetime import *

from app.models.event import Event
from app.models.user import User
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.models.interest import Interest
from app.logic.events import eventEdit, getEvents, deleteEvent, groupEventsByCategory, groupEventsByProgram
from app.logic.events import getAllFacilitators, getUpcomingEventsForUser

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
    assert events[1].description == "Training for Berea Buddies"
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
def test_deleteEvent():

    testingEvent = Event.create(eventName = "Testing delete event",
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

    testingEvent = Event.get(Event.eventName == "Testing delete event")

    program = 1
    eventId = testingEvent.id
    deletingEvent = deleteEvent(program, eventId)
    assert Event.get_or_none(Event.id == eventId) is None

    deletingEvent = deleteEvent(program, eventId)
    assert Event.get_or_none(Event.id == eventId) is None

@pytest.mark.integration
def test_beforeEdit():
    eventId = 4
    beforeEdit = Event.get_by_id(eventId)

    assert beforeEdit.eventName == "First Meetup"

@pytest.mark.integration
def test_afterEdit():
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
                    "eventEndDate": "2022 6 12"
                }
    newEventData.update(valid=True, eventFacilitator=User.get(User.username == 'ramsayb2'))
    eventFunction = eventEdit(newEventData)
    afterEdit = Event.get_by_id(newEventData['eventId'])
    assert afterEdit.description == "This is a Test"
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
                    "eventEndDate": "2022 6 12"
                }
    newEventData.update(valid=True, eventFacilitator=User.get(User.username == 'ramsayb2'))
    eventFunction = eventEdit(newEventData)
    afterEdit = Event.get_by_id(newEventData['eventId'])

    assert afterEdit.description == "Berea Buddies First Meetup"

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
    assert groupEventsByProgram(studentLedEvents) == {Program.get_by_id(1): [Event.get_by_id(1), Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(8),Event.get_by_id(9)]}

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
    assert "Empty Bowls Spring" == events[0].eventName

    user = "ramsayb2"
    events = getUpcomingEventsForUser(user, asOf=testDate)
    assert len(events) == 5
    assert "Making Bowls" == events[0].eventName


@pytest.mark.integration
def test_userWithNoInterestedEvent():

    user ="asdfasd" #invalid user
    events = getUpcomingEventsForUser(user)
    assert len(events) == 0

    user = "ayisie" #no interest selected
    events = getUpcomingEventsForUser(user)
    assert len(events) == 0

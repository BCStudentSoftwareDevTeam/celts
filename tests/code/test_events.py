import pytest
from flask import g
from app import app
from peewee import DoesNotExist, OperationalError, IntegrityError, fn
from datetime import datetime, date, timedelta
from dateutil import parser
from werkzeug.datastructures import MultiDict

from app.models import mainDB
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.eventTemplate import EventTemplate
from app.models.requirementMatch import RequirementMatch
from app.models.certificationRequirement import CertificationRequirement
from app.models.program import Program
from app.models.programBan import ProgramBan
from app.models.term import Term
from app.models.interest import Interest
from app.models.eventRsvp import EventRsvp
from app.models.note import Note

from app.logic.events import preprocessEventData, validateNewEventData, calculateRecurringEventFrequency
from app.logic.events import attemptSaveEvent, saveEventToDb, cancelEvent, deleteEvent, getParticipatedEventsForUser
from app.logic.events import calculateNewrecurringId, getPreviousRecurringEventData, getUpcomingEventsForUser
from app.logic.events import deleteEventAndAllFollowing, deleteAllRecurringEvents, getEventRsvpCountsForTerm, getEventRsvpCount
from app.logic.volunteers import addVolunteerToEventRsvp, updateEventParticipants
from app.logic.participants import addPersonToEvent
from app.logic.users import addUserInterest, removeUserInterest, banUser
from app.logic.utils import format24HourTime

@pytest.mark.integration
def test_event_model():
    event = Event.get_by_id(11)
    assert event.isPast

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
def test_preprocessEventData_checkboxes():

    # test that there is a return
    assert preprocessEventData({})

    # tets for return type
    assert type(preprocessEventData({}))== type({})

    # test for no keys
    eventData = {}
    newData = preprocessEventData(eventData)
    assert newData['isRsvpRequired'] == False
    assert newData['isService'] == False
    assert newData['isTraining'] == False

    eventData = {'isRsvpRequired':'', 'isRecurring': 'on', 'isService':True }
    newData = preprocessEventData(eventData)
    assert newData['isTraining'] == False
    assert newData['isRsvpRequired'] == False
    assert newData['isService'] == True
    assert newData['isRecurring'] == True

@pytest.mark.integration
def test_preprocessEventData_dates():

    eventData = {'startDate':''}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == ''
    assert newData['endDate'] == ''

    eventData = {'startDate':'09/07/21', 'endDate': '2021-08-08', 'isRecurring': 'on'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == datetime.strptime("2021-09-07","%Y-%m-%d")
    assert newData['endDate'] == datetime.strptime("2021-08-08","%Y-%m-%d")

    # test different date formats
    eventData = {'startDate':parser.parse('09/07/21'), 'endDate': 75, 'isRecurring': 'on'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == datetime.strptime("2021-09-07","%Y-%m-%d")
    assert newData['endDate'] == ''

    # endDate should match startDate for non-recurring events
    eventData = {'startDate':'09/07/21', 'endDate': '2021-08-08'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == newData['endDate']

    eventData = {'startDate':'09/07/21', 'endDate': '2021-08-08', 'isRecurring': 'on'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] != newData['endDate']

@pytest.mark.integration
def test_preprocessEventData_term():

    eventData = {}
    preprocessEventData(eventData)
    assert 'term' not in eventData

    eventData = {'term': 5}
    preprocessEventData(eventData)
    assert eventData['term'] == Term.get_by_id(5)

    eventData = {'term': 'asdf'}
    preprocessEventData(eventData)
    assert eventData['term'] == ''

@pytest.mark.integration
def test_preprocessEventData_requirement():
    with mainDB.atomic() as transaction:
        RequirementMatch.create(event=1, requirement=3)

        # key doesn't exist, no event id
        eventData = {}
        preprocessEventData(eventData)
        assert 'certRequirement' not in eventData

        # key doesn't exist, event id exists, requirement doesn't exist
        eventData = {'id': 11}
        preprocessEventData(eventData)
        assert 'certRequirement' not in eventData

        # key doesn't exist, event id exists, requirement exists
        eventData = {'id': 1}
        preprocessEventData(eventData)
        assert eventData['certRequirement'] == CertificationRequirement.get_by_id(3)

        # key exists, but requirement doesn't exist
        eventData = {'certRequirement': 73}
        preprocessEventData(eventData)
        assert eventData['certRequirement'] == ''

        # key is integer, requirement exists
        eventData = {'certRequirement': 3}
        preprocessEventData(eventData)
        assert eventData['certRequirement'] == CertificationRequirement.get_by_id(3)

        # key is object
        eventData = {'certRequirement': CertificationRequirement.get_by_id(3)}
        preprocessEventData(eventData)
        assert eventData['certRequirement'] == CertificationRequirement.get_by_id(3)

        transaction.rollback()

@pytest.mark.integration
def test_correctValidateNewEventData():

    eventData =  {'isFoodProvided': False, 'isRsvpRequired': False, 'isService': False,
                  'isTraining': True,'isRecurring': False,'startDate': parser.parse('1999-12-12'),
                  'endDate': parser.parse('2022-06-12'),'programId': 1,'location': "a big room",
                  'timeEnd': '06:00', 'timeStart': '04:00','description': "Empty Bowls Spring 2021",
                  'name': 'Empty Bowls Spring Event 1','term': 1,'contactName': "Kaidou of the Beast",'contactEmail': 'beastpirates@gmail.com'}

    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == True
    assert eventErrorMessage == "All inputs are valid."

@pytest.mark.integration
def test_wrongValidateNewEventData():
    eventData =  {'isFoodProvided': False, 'isRsvpRequired':False, 'isService':False,
                  'isTraining':True, 'isRecurring':False, 'programId':1, 'location':"a big room",
                  'timeEnd':'12:00', 'timeStart':'15:00', 'description':"Empty Bowls Spring 2021",
                  'name':'Empty Bowls Spring Event 1','term':1,'contactName': "Big Mom", 'contactEmail': 'weeeDDDINgCAKKe@gmail.com'}

    eventData['isRecurring'] = True
    eventData['startDate'] = parser.parse('2021-12-12')
    eventData['endDate'] = parser.parse('2021-06-12')
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == False
    assert eventErrorMessage == "Event start date is after event end date."

    # testing checks for raw form data
    eventData["startDate"] = parser.parse('2021-10-12')
    eventData['endDate'] = parser.parse('2022-06-12')
    for boolKey in ['isRsvpRequired', 'isTraining', 'isService', 'isRecurring']:
        eventData[boolKey] = 'on'
        isValid, eventErrorMessage = validateNewEventData(eventData)
        assert isValid == False
        assert eventErrorMessage == "Raw form data passed to validate method. Preprocess first."
        eventData[boolKey] = False

    # testing event starts after it ends.
    eventData["startDate"] = parser.parse('2021-06-12')
    eventData["endDate"] = parser.parse('2021-06-12')
    eventData["timeStart"] =  '21:39'
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == False
    assert eventErrorMessage == "Event end time must be after start time."

    # testing same event already exists if no event id
    eventData["startDate"] = parser.parse('2021-10-12')
    eventData["endDate"] = parser.parse('2022-06-12')
    eventData["location"] = "Seabury Center"
    eventData["timeStart"] = '18:00'
    eventData["timeEnd"] =  '21:00'
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == False
    assert eventErrorMessage == "This event already exists"

    # If we provide an event id, don't check for existence
    eventData['id'] = 5
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid

@pytest.mark.integration
def test_calculateRecurringEventFrequency():

    eventInfo = {'name': "testEvent",
                 'startDate': parser.parse("02/22/2023"),
                 'endDate': parser.parse("03/9/2023")}

    # test correct response
    returnedEvents = calculateRecurringEventFrequency(eventInfo)
    assert returnedEvents[0] == {'name': 'testEvent Week 1', 'date': parser.parse('02/22/2023'), 'week': 1}
    assert returnedEvents[1] == {'name': 'testEvent Week 2', 'date': parser.parse('03/01/2023'), 'week': 2}
    assert returnedEvents[2] == {'name': 'testEvent Week 3', 'date': parser.parse('03/08/2023'), 'week': 3}

    # test non-datetime
    eventInfo["startDate"] = '2021/06/07'
    with pytest.raises(Exception):
        returnedEvents = calculateRecurringEventFrequency(eventInfo)

    # test non-recurring
    eventInfo["startDate"] = '2021/06/07'
    eventInfo["endDate"] = '2021/06/07'
    with pytest.raises(Exception):
        returnedEvents = calculateRecurringEventFrequency(eventInfo)

@pytest.mark.integration
def test_attemptSaveEvent():
    # This test duplicates some of the saving tests, but with raw data, like from a form
    eventInfo =  { 'isTraining':'on', 'isRecurring':False, 'recurringId':None,
                   'startDate': '2021-12-12',
                   'rsvpLimit': None,
                   'endDate':'2022-06-12', 'location':"a big room",
                   'timeEnd':'09:00 PM', 'timeStart':'06:00 PM',
                   'description':"Empty Bowls Spring 2021",
                   'name':'Attempt Save Test','term':1,'contactName':"Garrett D. Clark",
                   'contactEmail': 'boorclark@gmail.com'}
    eventInfo['program'] = Program.get_by_id(1)

    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            success, errorMessage = attemptSaveEvent(eventInfo)
        if not success:
            pytest.fail(f"Save failed: {errorMessage}")

        try:
            event = Event.get(name="Attempt Save Test")

        except Exception as e:
            pytest.fail(str(e))

        finally:
            transaction.rollback() # undo our database changes

@pytest.mark.integration
def test_saveEventToDb_create():

    eventInfo =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False,
                  'isTraining':True, 'isRecurring':False,'isAllVolunteerTraining': True, 'recurringId':None, 'startDate': parser.parse('2021-12-12'),
                   'endDate':parser.parse('2022-06-12'), 'location':"a big room",
                   'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                   'name':'Empty Bowls Spring','term':1,'contactName':"Finn D. Bledsoe", 'contactEmail': 'finnimanBledsoe@pigeoncarrier.com'}
    eventInfo['program'] = Program.get_by_id(1)

    # if valid is not added to the dict
    with pytest.raises(Exception):
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            saveEventToDb(eventInfo)

    # if 'valid' is not True
    eventInfo['valid'] = False
    with pytest.raises(Exception):
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            saveEventToDb(eventInfo)

    #test that the event is added successfully
    with mainDB.atomic() as transaction:
        eventInfo['valid'] = True
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            createdEvents = saveEventToDb(eventInfo)
        assert len(createdEvents) == 1
        assert createdEvents[0].program.id == 1 # 

        transaction.rollback()

@pytest.mark.integration
def test_saveEventToDb_recurring():
    with mainDB.atomic() as transaction:
        with app.app_context():
            eventInfo =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRecurring': True, 'recurringId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate':parser.parse('01-18-2022'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}

            eventInfo['valid'] = True
            eventInfo['program'] = Program.get_by_id(1)

            g.current_user = User.get_by_id("ramsayb2")
            createdEvents = saveEventToDb(eventInfo)
            assert len(createdEvents) == 6

            transaction.rollback()

@pytest.mark.integration
def test_saveEventToDb_update():
    with mainDB.atomic() as transaction:

        eventId = 4
        beforeUpdate = Event.get_by_id(eventId)
        assert beforeUpdate.name == "First Meetup"

        # Verify description, cerRequirement, and isRsvpRequried are updated for event 4 and 
        # program, isAllVolunteerTraining, and recurringId are not updated.  
        newEventData = {
                        "id": 4,
                        "program": 1,
                        "term": 1,
                        "name": "First Meetup",
                        "description": "This is a Test",
                        "timeStart": "06:00 PM",
                        "timeEnd": "09:00 PM",
                        "certRequirement": 9,
                        "location": "House",
                        'isFoodProvided': False,
                        'isRecurring': True,
                        'recurringId': 3,
                        'isTraining': True,
                        'isRsvpRequired': True,
                        'rsvpLimit': None,
                        'isAllVolunteerTraining': True,
                        'isService': False,
                        "startDate": "2021-12-12",
                        "endDate": "2022-6-12",
                        "contactName": "Monkey D. Luffy",
                        "contactEmail": "goatpiece@berea.edu",
                        "valid": True
                    }
        
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            saveEventToDb(newEventData)
        afterUpdate = Event.get_by_id(newEventData['id'])
        assert afterUpdate.description == "This is a Test"
        assert afterUpdate.isRsvpRequired == True
        
        assert afterUpdate.program == Program.get_by_id(2)
        assert afterUpdate.recurringId is None
        assert afterUpdate.isAllVolunteerTraining == False
        assert RequirementMatch.select().where(RequirementMatch.event == afterUpdate,
                                               RequirementMatch.requirement == 9).exists()
        
        newEventData['description'] = "Berea Buddies First Meetup"

        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            saveEventToDb(newEventData)
        afterUpdate = Event.get_by_id(newEventData['id'])
        assert afterUpdate.description == "Berea Buddies First Meetup"
        

        transaction.rollback()

@pytest.mark.integration
def test_cancelEvent():
     with mainDB.atomic() as transaction:
        # creates an event 
        testingEvent = Event.create(name = "Testing canceled event",
                                    term = 2,
                                    description = "This Event is Created to be Canceled.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = "2021-12-12",
                                    endDate = "2022-6-12",
                                    isCanceled = False,
                                    program = 2)
        
        testingEvent = Event.get(Event.name == "Testing canceled event")
        eventId = testingEvent.id
        

        with app.test_request_context():
            g.current_user = User.get_by_id("ramsayb2")
            cancelEvent(eventId)
        
        event = Event.get(Event.id == eventId)
        assert event.isCanceled
        transaction.rollback()


@pytest.mark.integration
def test_deleteEvent():
    with mainDB.atomic() as transaction:
        # creates non recurring event
        testingEvent = Event.create(name = "Testing delete event",
                                    term = 2,
                                    description = "This Event is Created to be Deleted.",
                                    timeStart = "06:00 PM",
                                    timeEnd = "09:00 PM",
                                    location = "No Where",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = "2021-12-12",
                                    endDate = "2022-6-12",
                                    recurringId = None,
                                    program = 9)

        testingEvent = Event.get(Event.name == "Testing delete event")
        eventId = testingEvent.id

        # tests deletion of standard event
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEvent(eventId)
        assert Event.get_or_none(Event.id == eventId) is None

        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEvent(eventId)
        assert Event.get_or_none(Event.id == eventId) is None
        transaction.rollback()

        # creates a recurring event
        eventInfo =  {'isFoodProvided': False,
                      'isRsvpRequired': False,
                      'rsvpLimit': None,
                      'isService': False,
                      'isAllVolunteerTraining': True,
                      'isTraining': True,
                      'isRecurring': True,
                      'recurringId': 20,
                      'startDate': parser.parse('12-12-2021'),
                      'endDate': parser.parse('01-18-2022'),
                      'location': "Your pet rubber ducks little pond",
                      'timeEnd': '09:00 PM',
                      'timeStart': '06:00 PM',
                      'description': "Empty Bowls Spring 2021",
                      'name': 'Not Empty Bowls Spring',
                      'term': 1,
                      'contactEmail': '',
                      'contactName': ''}

        eventInfo['valid'] = True
        eventInfo['program'] = Program.get_by_id(1)
        createdEvents = saveEventToDb(eventInfo)
        event = Event.get_by_id(createdEvents[0].id)
        recurringId = event.recurringId

        # check how many events exist before event deletion
        recurringEventsBefore = list(Event.select().where(Event.recurringId==recurringId).order_by(Event.recurringId))
        for counter, recurring in enumerate(recurringEventsBefore):
            assert recurring.name == ("Not Empty Bowls Spring Week " + str(counter + 1))

        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEvent(createdEvents[0])

        # check how many events exist after event deletion and make sure they are linear
        recurringEventsAfter = list(Event.select().where(Event.recurringId==recurringId).order_by(Event.recurringId))

        for count, recurring in enumerate(recurringEventsAfter):
            assert recurring.name == ("Not Empty Bowls Spring Week " + str(count + 1))
        assert (len(recurringEventsBefore)-1) == len(recurringEventsAfter)
        transaction.rollback()

        #creating recurring event again to test def deleteRecurringSeries()
        eventInfo['valid'] = True
        eventInfo['program'] = Program.get_by_id(1)
        recurringEvents = saveEventToDb(eventInfo)
        eventIdToDelete = Event.get_by_id(recurringEvents[3].id)
        recurringId = event.recurringId

        totalRecurringEvents = len(Event.select().where(Event.recurringId == recurringId))
        #checks the number of all recurring events that will take place after a recurring event plus the event itself.
        eventPlusAllRecurringEventsAfter = len(Event.select().where((Event.recurringId == recurringId) & (Event.startDate >= eventIdToDelete.startDate)))

        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEventAndAllFollowing(eventIdToDelete)
            totalRecurringEventsAfter = len(Event.select().where(Event.recurringId == recurringId))
        assert (totalRecurringEvents - eventPlusAllRecurringEventsAfter) == totalRecurringEventsAfter
        transaction.rollback()

        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteAllRecurringEvents(eventIdToDelete)
            newTotalRecurringEvents = len(Event.select().where(Event.recurringId == recurringId))
        assert newTotalRecurringEvents == 0

@pytest.mark.integration
def test_upcomingEvents():
    with mainDB.atomic() as transaction:
        testDate = datetime.strptime("2021-08-01 05:00","%Y-%m-%d %H:%M")
        dayBeforeTestDate = testDate - timedelta(days=1)

        # Create a user to run the tests with
        user = User.create(username = 'usrtst',
                           firstName = 'Test',
                           lastName = 'User',
                           bnumber = '03522492',
                           email = 'usert@berea.deu',
                           isStudent = True)

        # Create an event that is not a part of a program the user can RSVP to
        noProgram = Event.create(name = "Upcoming event with no program",
                                 term = 2,
                                 description = "Test upcoming no program event.",
                                 location = "The moon",
                                 startDate = testDate,
                                 endDate = testDate + timedelta(days=1),
                                 program = 9)

         # Create a new Program to create the new Program Event off of so the
        # user can mark interest for it
        programForInterest = Program.create(id = 13,
                                            programName = "BOO",
                                            isStudentLed = False,
                                            isBonnerScholars = False,
                                            contactEmail = "test@email",
                                            contactName = "testName")
        programForInterest2 = Program.create(id = 14,
                                           programName = "BOO2",
                                           isStudentLed = False,
                                           isBonnerScholars = False,
                                           contactEmail = "test@email",
                                           contactName = "testName")
        programForBanning = Program.create(id = 15,
                                           programName = "BANNED",
                                           isStudentLed = False,
                                           isBonnerScholars = False,
                                           contactEmail = "test@email",
                                           contactName = "testName")
        
        
        
        # Create a Program Event to show up when the user marks interest in a
        # new program
        newProgramEvent = Event.create(name = "Upcoming event with program",
                                       term = 2,
                                       description = "Test upcoming program event.",
                                       location = "The sun",
                                       startDate = testDate,
                                       endDate = testDate + timedelta(days=1),
                                       program = programForInterest2)

        newBannedProgramEvent = Event.create(name = "Upcoming event with banned program",
                                             term = 2,
                                             description = "Test upcoming banned program event.",
                                             location = "The moon",
                                             startDate = testDate,
                                             endDate = testDate + timedelta(days=1),
                                             program= programForBanning)

        newRecurringEvent = Event.create(name = "Recurring Event Test",
                                         term = 2,
                                         description = "Test upcoming program event.",
                                         location = "The sun",
                                         startDate = date(2021,12,12),
                                         endDate = date(2021,12,14),
                                         recurringId = 1,
                                         program= programForInterest)

        newRecurringSecond = Event.create(name = "Recurring second event",
                                          term = 2,
                                          description = "Test upcoming program event.",
                                          location = "The sun",
                                          startDate = date(2021,12,14),
                                          endDate = date(2021,12,15),
                                          recurringId = 1,
                                          program= programForInterest)

        newRecurringDifferentId = Event.create(name = "Recurring different Id",
                                               term = 2,
                                               description = "Test upcoming program event.",
                                               location = "The sun",
                                               startDate = date(2021,12,13),
                                               endDate = date(2021,12,13),
                                               recurringId = 2,
                                               program= programForInterest)

        # User has not RSVPd and is Interested
        addUserInterest(programForInterest.id, user)
        addUserInterest(programForInterest2.id, user)
        addUserInterest(programForBanning.id, user)
        eventsInUserInterestedProgram = getUpcomingEventsForUser(user, asOf = testDate)

        assert newProgramEvent in eventsInUserInterestedProgram
        assert newRecurringDifferentId in eventsInUserInterestedProgram
        assert newRecurringEvent in eventsInUserInterestedProgram
        assert newRecurringSecond not in eventsInUserInterestedProgram

        # Programs the user is banned from do not have their events showing up in
        # their upcoming events
        banUser(programForBanning.id, user.username, "Test banned program", testDate, "ramsayb2")
        eventsUserNotBannedFrom = getUpcomingEventsForUser(user, asOf = testDate)
        assert newBannedProgramEvent in eventsInUserInterestedProgram
        assert newBannedProgramEvent not in eventsUserNotBannedFrom

        # Programs the user has been unbanned from do have their events showing up
        # in their upcoming events
        noteForUnban = Note.create(createdBy = "ramsayb2",
                                   createdOn = dayBeforeTestDate,
                                   noteContent = "The test user is unbanned.",
                                   isPrivate = 0)
        (ProgramBan.update(endDate = dayBeforeTestDate,unbanNote = noteForUnban)
                   .where(ProgramBan.program == programForBanning.id,
                          ProgramBan.user == user.username).execute())

        assert newBannedProgramEvent in getUpcomingEventsForUser(user, asOf = testDate)

        # user has RSVPd and is Interested
        EventRsvp.create(event=noProgram, user=user)
        getUpcomingEventsForUser(user, asOf = testDate)

        interestAndRsvp = eventsInUserInterestedProgram + [noProgram]
        for event in eventsInUserInterestedProgram:
            assert event in interestAndRsvp

        # User has RSVPd and is not Interested
        removeUserInterest(programForInterest.id, user)
        removeUserInterest(programForInterest2.id, user)
        removeUserInterest(programForBanning.id, user)
        eventsInUserRsvp = getUpcomingEventsForUser(user, asOf = testDate)
        assert eventsInUserRsvp == [noProgram]

        # Get upcoming for specific program only
        # we would have multiples with interests in both programs, but we specify only one
        addUserInterest(programForInterest.id, user)
        addUserInterest(programForInterest2.id, user)
        eventsInProgram = getUpcomingEventsForUser(user, program = programForInterest2.id, asOf = testDate)

        assert eventsInProgram == [newProgramEvent]

        transaction.rollback()

@pytest.mark.integration
def test_volunteerHistory():
    with mainDB.atomic() as transaction:

        # Create a user to run the tests with
        user = User.create(username = 'usrtst',
                           firstName = 'Test',
                           lastName = 'User',
                           bnumber = '03522492',
                           email = 'usert@berea.deu',
                           isStudent = True)


        # Create a program that will have the program event created off of it
        participatedProgram = Program.create(id = 13,
                                             programName = "BOO",
                                             isStudentLed = False,
                                             isBonnerScholars = False,
                                             contactEmail = "test@email",
                                             contactName = "testName",)
        
        # Create a program event in the past that the test user will have
        # participated in
        participatedProgramEvent = Event.create(name = "Attended program event",
                                                term = 2,
                                                description = "Test attended program event.",
                                                timeStart = "18:00:00",
                                                timeEnd = "21:00:00",
                                                location = "The moon",
                                                startDate = "2021-12-12",
                                                endDate = "2021-12-13",
                                                isAllVolunteerTraining = False,
                                                program = participatedProgram)
        # Create a non-program event in the past that the test user will have
        # participated in
        participatedEvent = Event.create(name = "Attended event",
                                         term = 2,
                                         description = "Test attended event.",
                                         timeStart = "18:00:00",
                                         timeEnd = "21:00:00",
                                         location = "The moon",
                                         startDate = "2021-12-12",
                                         endDate = "2021-12-13",
                                         isAllVolunteerTraining = False,
                                         program = 9)

        # Add the created user as a participnt to the created program event
        EventParticipant.create(user = user , event = participatedProgramEvent.id)
        assert participatedProgramEvent in getParticipatedEventsForUser(user)

        # Add the created user as a participant to the create non-program event
        EventParticipant.create(user = user, event = participatedEvent.id)
        assert participatedEvent in getParticipatedEventsForUser(user)

        # Make sure an event that is not supposed to be returned isnt
        assert Event.get_by_id(1) not in getParticipatedEventsForUser(user)

        transaction.rollback()

@pytest.mark.integration
def test_format24HourTime():

    # tests valid "input times"
    assert format24HourTime('08:00 AM') == "08:00"
    assert format24HourTime('5:38 AM') == "05:38"
    assert format24HourTime('05:00 PM') == "17:00"
    assert format24HourTime('7:30 PM') == "19:30"
    assert format24HourTime('12:32 PM') == "12:32"
    assert format24HourTime('12:01 AM') == "00:01"
    assert format24HourTime('12:32') == "12:32"
    assert format24HourTime('00:01') == "00:01"
    assert format24HourTime('17:07') == "17:07"
    assert format24HourTime('23:59') == "23:59"
    time = datetime(1900, 1, 1, 8, 30)
    assert format24HourTime(time) == "08:30"
    time = datetime(1900, 1, 1, 23, 59)
    assert format24HourTime(time) == "23:59"
    time = datetime(1900, 1, 1, 00, 1)
    assert format24HourTime(time) == "00:01"

    # tests "input times" that are not valid inputs
    with pytest.raises(ValueError):
        assert format24HourTime('13:30 PM')
        assert format24HourTime('13:30 AM')
        assert format24HourTime(':30')
        assert format24HourTime('01:30:00 PM')
        assert format24HourTime('Clever String')

@pytest.mark.integration
def test_calculateNewrecurringId():

    maxRecurringId = Event.select(fn.MAX(Event.recurringId)).scalar()
    if maxRecurringId == None:
        maxRecurringId = 1
    else:
        maxRecurringId += 1
    assert calculateNewrecurringId() == maxRecurringId

@pytest.mark.integration
def test_getPreviousRecurringEventData():
    with mainDB.atomic() as transaction:

        testingEvent1 = Event.create(name = "Testing delete event",
                                     term = 2,
                                     description = "This Event is Created to be Deleted.",
                                     timeStart = "6:00 pm",
                                     timeEnd = "9:00 pm",
                                     location = "No Where",
                                     isRsvpRequired = 0,
                                     isTraining = 0,
                                     isService = 0,
                                     startDate = "2021-12-5",
                                     endDate = "2022-12-5",
                                     recurringId = 3,
                                     program = 9)
        testingEvent2 = Event.create(name = "Testing delete event",
                                     term = 2,
                                     description = "This Event is Created to be Deleted.",
                                     timeStart = "6:00 pm",
                                     timeEnd = "9:00 pm",
                                     location = "No Where",
                                     isRsvpRequired = 0,
                                     isTraining = 0,
                                     isService = 0,
                                     startDate = "2022-12-12",
                                     endDate = "2022-12-12",
                                     recurringId = 3,
                                     program = 9)
        testingEvent3 = Event.create(name = "Testing delete event",
                                     term = 2,
                                     description = "This Event is Created to be Deleted.",
                                     timeStart = "6:00 pm",
                                     timeEnd = "9:00 pm",
                                     location = "No Where",
                                     isRsvpRequired = 0,
                                     isTraining = 0,
                                     isService = 0,
                                     startDate = "2022-12-19",
                                     endDate = "2022-12-19",
                                     recurringId = 3,
                                     program = 9)

        EventParticipant.create(user = User.get_by_id("neillz"),
                                                      event = testingEvent2.id,
                                                      hoursEarned = None)
        EventParticipant.create(user = User.get_by_id("ramsayb2"),
                                                      event = testingEvent2.id,
                                                      hoursEarned = None)
        EventParticipant.create(user = User.get_by_id("khatts"),
                                                      event = testingEvent2.id,
                                                      hoursEarned = None)

        val = getPreviousRecurringEventData(testingEvent3.recurringId)
        assert val[0].username == "neillz"
        assert val[1].username == "ramsayb2"
        assert val[2].username == "khatts"
        transaction.rollback()

@pytest.mark.integration
def test_getEventRsvpCountsForTerm():
    with mainDB.atomic() as transaction:
        eventWithRsvpLimit = Event.create(name = "Req and Limit",
                                          term = 2,
                                          description = "Event that requries RSVP and has an RSVP limit set.",
                                          timeStart = "6:00 pm",
                                          timeEnd = "9:00 pm",
                                          location = "The Moon",
                                          isRsvpRequired = 1,
                                          rsvpLimit = 4,
                                          startDate = "2022-12-19",
                                          endDate = "2022-12-19",
                                          program = 9)

        testUserToRsvp = User.create(username = 'rsvpUsr',
                                     firstName = 'RSVP',
                                     lastName = 'Test',
                                     bnumber = '48616874',
                                     email = 'helloThere@berea.edu',
                                     isStudent = True,
                                     )

        limit = getEventRsvpCountsForTerm(Term.get_by_id(2))
        assert limit[eventWithRsvpLimit.id] == 0

        EventRsvp.create(event=eventWithRsvpLimit, user=testUserToRsvp)

        limit = getEventRsvpCountsForTerm(Term.get_by_id(2))
        assert limit[eventWithRsvpLimit.id] == 1

        transaction.rollback()

@pytest.mark.integration
def test_getEventRsvpCount():
    with mainDB.atomic() as transaction:

        eventWithRsvp = Event.create(name = "Req and Limit",
                                     term = 2,
                                     description = "Event that requries RSVP and has an RSVP limit set.",
                                     timeStart = "6:00 pm",
                                     timeEnd = "9:00 pm",
                                     location = "The Moon",
                                     isRsvpRequired = 1,
                                     startDate = "2022-12-19",
                                     endDate = "2022-12-19",
                                     program = 9)
        user_list = []
        for i in range(5):
            user_list.append(User.create(username = f'rsvpUsr{i}',
                             firstName = f'RSVP{i}',
                             lastName = f'Test{i}',
                             bnumber = f'4861687{i}',
                             email = f'helloThere{i}@berea.edu',
                             isStudent = True,
                            ))

        EventRsvp.create(event=Event.get_by_id(1), user=user_list[0])

        rsvpd_user_count = getEventRsvpCount(eventWithRsvp.id)
        assert rsvpd_user_count == 0
        for index, user in enumerate(user_list):
            EventRsvp.create(event=eventWithRsvp, user=user)
            rsvpd_user_count = getEventRsvpCount(eventWithRsvp.id)
            assert rsvpd_user_count == (index + 1)

        transaction.rollback()

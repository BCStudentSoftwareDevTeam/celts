import pytest
import json
from flask import g, session
from app import app
from peewee import DoesNotExist, OperationalError, IntegrityError, fn
from playhouse.shortcuts import model_to_dict
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
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

from app.logic.events import preprocessEventData, validateNewEventData, getRepeatingEventsData
from app.logic.events import attemptSaveEvent, attemptSaveMultipleOfferings, saveEventToDb, cancelEvent, deleteEvent, getParticipatedEventsForUser
from app.logic.events import calculateNewSeriesId, getPreviousSeriesEventData, getUpcomingEventsForUser, calculateNewSeriesId
from app.logic.events import deleteEventAndAllFollowing, deleteAllEventsInSeries, getEventRsvpCountsForTerm, getEventRsvpCount, getCountdownToEvent, copyRsvpToNewEvent
from app.logic.volunteers import updateEventParticipants
from app.logic.participants import addPersonToEvent
from app.logic.users import addUserInterest, removeUserInterest, banUser
from app.logic.utils import format24HourTime

@pytest.mark.integration
def test_event_end():
    with mainDB.atomic() as transaction:
        # creates an event in the future
        testingEvent = Event.create(name = "Testing event start/end time",
                                    term = 2,
                                    description = "This Event is Created to be Deleted.",
                                    timeStart = datetime.now() + timedelta(seconds=-2),
                                    timeEnd = datetime.now() + timedelta(seconds=2),
                                    location = "No Where",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = datetime.now() + timedelta(days=1),
                                    endDate = datetime.now() + timedelta(days=2),
                                    seriesId = None,
                                    program = 9)
        testingEvent = Event.get_by_id(testingEvent.id)

        assert testingEvent.isPastEnd == False
        assert testingEvent.isPastStart == False
        transaction.rollback()

    with mainDB.atomic() as transaction:
        # creates an event in the present
        testingEvent = Event.create(name = "Testing event start/end time",
                                    term = 2,
                                    description = "This Event is Created to be Deleted.",
                                    timeStart = datetime.now() + timedelta(seconds=-2),
                                    timeEnd = datetime.now() + timedelta(seconds=2),
                                    location = "No Where",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = datetime.now(),
                                    endDate = datetime.now() + timedelta(days=1),
                                    seriesId = None,
                                    program = 9)
        testingEvent = Event.get_by_id(testingEvent.id)

        assert testingEvent.isPastEnd == False
        assert testingEvent.isPastStart == True
        transaction.rollback()

    with mainDB.atomic() as transaction:
        # creates an event in the past
        testingEvent = Event.create(name = "Testing event start/end time",
                                    term = 2,
                                    description = "This Event is Created to be Deleted.",
                                    timeStart = datetime.now() + timedelta(seconds=-2),
                                    timeEnd = datetime.now() + timedelta(seconds=2),
                                    location = "No Where",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = datetime.now() + timedelta(days=-3),
                                    endDate = datetime.now() + timedelta(days=-1),
                                    seriesId = None,
                                    program = 9)
        testingEvent = Event.get_by_id(testingEvent.id)

        assert testingEvent.isPastEnd == True
        assert testingEvent.isPastStart == True
        transaction.rollback()



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
    assert newData['isFoodProvided'] == False
    assert newData['isRsvpRequired'] == False
    assert newData['isTraining'] == False
    assert newData['isService'] == False
    assert newData['isRepeating'] == False
    

    
    eventData = {'isRsvpRequired':'', 'isRepeating': 'on', 'isService':True}
    newData = preprocessEventData(eventData)
    assert newData['isTraining'] == False
    assert newData['isRsvpRequired'] == False
    assert newData['isService'] == True
    assert newData['isRepeating'] == True

@pytest.mark.integration
def test_preprocessEventData_dates():

    eventData = {'startDate':''}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == ''
    assert newData['endDate'] == ''

    eventData = {'startDate':'09/07/21', 'endDate': '2021-08-08', 'isRepeating': 'on'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == datetime.strptime("2021-09-07","%Y-%m-%d")
    assert newData['endDate'] == datetime.strptime("2021-08-08","%Y-%m-%d")

    # test different date formats
    eventData = {'startDate':parser.parse('09/07/21'), 'endDate': 75, 'isRepeating': 'on'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == datetime.strptime("2021-09-07","%Y-%m-%d")
    assert newData['endDate'] == ''

    # non-repeating events do not have any end dates
    eventData = {'startDate':'09/07/21', 'endDate': ''}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == datetime.strptime("2021-09-07","%Y-%m-%d")
    assert newData['endDate'] == ''

    #repeating events have end dates
    eventData = {'startDate':'09/07/21', 'endDate': '2021-08-08', 'isRepeating': 'on'}
    newData = preprocessEventData(eventData)
    assert newData['startDate'] == datetime.strptime("2021-09-07","%Y-%m-%d")
    assert newData['endDate'] == datetime.strptime("2021-08-08","%Y-%m-%d")
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
def test_preprocessEventData_seriesData():
    # When there is no seriesData we should get a jsonified empty list
    eventData = preprocessEventData({})
    assert eventData['seriesData'] == json.dumps([])

    # Test parsing from list
    offeringData = [
                        {
                            'eventName': 'Offering 1',
                            'startDate': 'Today',
                            'timeStart': '01:00 PM',
                            'timeEnd': '02:00 PM',
                            'isDuplicate': False
                        }
                    ]
    eventData = preprocessEventData({'seriesData': offeringData})
    assert eventData['seriesData'] == json.dumps(offeringData)

    # Test when data is missing/invalid
    offeringData = [
                        {}, # Empty event offering should be filled with defaults
                        {
                            'eventName': 'Offering 1',
                            'startDate': 'Today',
                            'timeStart': 1, # Wrong format and type
                            #'timeEnd': '02:00 PM'  (No end time provided)
                            'isDuplicate': True
                        }
                    ]
    eventData = preprocessEventData({'seriesData': offeringData})
    offering = json.loads(eventData['seriesData'])[1]
    assert offering['eventName'] == 'Offering 1'
    assert offering['startDate'] == 'Today'
    assert offering['timeStart'] == ''
    assert offering['timeEnd'] == ''
    assert offering['isDuplicate'] == True
    defaultOffering = json.loads(eventData['seriesData'])[0]
    assert defaultOffering['eventName'] == ''
    assert defaultOffering['startDate'] == ''
    assert defaultOffering['timeStart'] == ''
    assert defaultOffering['timeEnd'] == ''
    assert defaultOffering['isDuplicate'] == False
    


    # Test when data is already valid and stringified
    offeringData = json.dumps([
                        {
                            'eventName': 'Offering 1',
                            'startDate': 'Today',
                            'timeStart': '01:00 PM',
                            'timeEnd': '02:00 PM',
                            'isDuplicate': False
                        }
                    ])
    eventData = preprocessEventData({'seriesData': offeringData})
    offering = json.loads(eventData['seriesData'])[0]
    assert offering == json.loads(offeringData)[0]


@pytest.mark.integration
def test_correctValidateNewEventData():

    eventData =  {'isFoodProvided': False, 'isRsvpRequired': False, 'isService': False,
                  'isTraining': True,'isRepeating': False,'startDate': parser.parse('1999-12-12'),
                  'endDate': parser.parse('2022-06-12'),'programId': 1,'location': "a big room",
                  'timeEnd': '06:00', 'timeStart': '04:00','description': "Empty Bowls Spring 2021",
                  'name': 'Empty Bowls Spring Event 1','term': 1,'contactName': "Kaidou of the Beast",'contactEmail': 'beastpirates@gmail.com'}

    eventData['isRepeating'] = False
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == True
    assert eventErrorMessage == "All inputs are valid."

@pytest.mark.integration
def test_wrongValidateNewEventData():
    eventData =  {'isFoodProvided': False, 'isRsvpRequired':False, 'isService':False,
                  'isTraining':True, 'isRepeating':False, 'isSeries': False, 'programId':1, 'location':"a big room",
                  'timeEnd':'12:00', 'timeStart':'15:00', 'description':"Empty Bowls Spring 2021",
                  'name':'Empty Bowls Spring Event 1','term':1,'contactName': "Big Mom", 'contactEmail': 'weeeDDDINgCAKKe@gmail.com'}
    
    #repeating event 
    eventData['isSeries'] = True
    eventData['isRepeating'] = True
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == False
    assert eventErrorMessage == "Event end time must be after start time."
    
    #non-repeating series event
    eventData['isSeries'] = True
    eventData['isRepeating'] = False
    isValid, eventErrorMessage = validateNewEventData(eventData)
    assert isValid == False
    assert eventErrorMessage == "Event end time must be after start time."

    # testing checks for raw form data
    eventData["startDate"] = parser.parse('2021-10-12')
    eventData['endDate'] = parser.parse('2022-06-12')
    for boolKey in ['isRsvpRequired', 'isTraining', 'isService', 'isRepeating']:
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
    returnedEvents = getRepeatingEventsData(eventInfo)
    assert returnedEvents[0] == {'name': 'testEvent Week 1', 'date': parser.parse('02/22/2023'), 'week': 1}
    assert returnedEvents[1] == {'name': 'testEvent Week 2', 'date': parser.parse('03/01/2023'), 'week': 2}
    assert returnedEvents[2] == {'name': 'testEvent Week 3', 'date': parser.parse('03/08/2023'), 'week': 3}

    # test non-datetime
    eventInfo["startDate"] = '2021/06/07'
    with pytest.raises(Exception):
        returnedEvents = getRepeatingEventsData(eventInfo)

    # test non-recurring
    eventInfo["startDate"] = '2021/06/07'
    eventInfo["endDate"] = '2021/06/07'
    with pytest.raises(Exception):
        returnedEvents = getRepeatingEventsData(eventInfo)

@pytest.mark.integration
def test_attemptSaveEvent():
    # This test duplicates some of the saving tests, but with raw data, like from a form
    eventInfo =  { 'isTraining':'on', 'isRepeating':False, 'seriesId':None,
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
            savedEvents, errorMessage = attemptSaveEvent(eventInfo)
        if not savedEvents:
            pytest.fail(f"Save failed: {errorMessage}")

        try:
            event = Event.get(name="Attempt Save Test")

        except Exception as e:
            pytest.fail(str(e))

        finally:
            transaction.rollback() # undo our database changes


@pytest.mark.integration
def test_attemptSaveMultipleOfferings():
    baseEventData =  {
                    'isTraining':'on', 'isRepeating':False, 'seriesId': 1,
                    'startDate': '2021-12-12',
                    'rsvpLimit': None,
                    'endDate':'2022-06-12', 'location':"a big room",
                    'timeEnd':'09:00 PM', 'timeStart':'06:00 PM',
                    'description':"Empty Bowls Spring 2021",
                    'name':'Attempt Save Test','term':1,'contactName':"Garrett D. Clark",
                    'contactEmail': 'boorclark@gmail.com'
                    }
    
    baseEventData['program'] = Program.get_by_id(1)

    validseriesData = baseEventData.copy()
    validseriesData['seriesData'] = [{ 
                            'eventName': 'Offering 1',
                            'eventDate': '2022-06-12', 
                            'startTime': '09:00 PM',
                            'endTime': '10:00 PM', 
                          },
                          {
                            'eventName': 'Offering 2',
                            'eventDate': '2022-06-13', 
                            'startTime': '09:00 PM',
                            'endTime': '10:00 PM', 
                          },
                          {
                            'eventName': 'Offering 3',
                            'eventDate': '2022-06-16', 
                            'startTime': '09:00 PM',
                            'endTime': '10:00 PM', 
                          }]
    
    duplicatedseriesData = baseEventData.copy()
    duplicatedseriesData['seriesData'] = [{ 
                            'eventName': 'Offering 1',
                            'eventDate': '2022-06-12', 
                            'startTime': '09:00 PM',
                            'endTime': '10:00 PM', 
                          },
                          {
                            'eventName': 'Offering 1',
                            'eventDate': '2022-06-12', 
                            'startTime': '09:00 PM',
                            'endTime': '10:00 PM', 
                          },
                          {
                            'eventName': 'Offering 3',
                            'eventDate': '2022-06-16', 
                            'startTime': '09:00 PM',
                            'endTime': '10:00 PM', 
                          }]
    
    
    
    with mainDB.atomic() as transaction:
        # test valid data
        succeeded, savedEvents, failedSavedOfferings = attemptSaveMultipleOfferings(validseriesData, None)
        assert succeeded == True
        assert len(savedEvents) == 3
        assert len(failedSavedOfferings) == 0

        transaction.rollback()
        
        # test duplicated data
        succeeded, savedEvents, failedSavedOfferings = attemptSaveMultipleOfferings(duplicatedseriesData, None)
        assert succeeded == False
        assert len(savedEvents) == 0
        assert len(failedSavedOfferings) == 1

        transaction.rollback()


@pytest.mark.integration
def test_saveEventToDb_create():

    eventInfo =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False,
                  'isTraining':True, 'isRepeating': False,'isAllVolunteerTraining': True, 'seriesId':None, 'startDate': parser.parse('2021-12-12'),
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
def test_saveEventToDb_repeating():
    with mainDB.atomic() as transaction:
        with app.app_context():
            eventInfo_1 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': True, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate': parser.parse('12-12-2021'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}
            
            eventInfo_2 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': True, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate': parser.parse('12-12-2021'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}
            
            eventInfo_3 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': True, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate': parser.parse('12-12-2021'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}

            eventInfo_1['valid'] = True
            eventInfo_2['valid'] = True
            eventInfo_3['valid'] = True
            eventInfo_1['program'] = Program.get_by_id(1)
            eventInfo_2['program'] = Program.get_by_id(1)
            eventInfo_3['program'] = Program.get_by_id(1)

            g.current_user = User.get_by_id("ramsayb2")
            createdEvents = [
                saveEventToDb(eventInfo_1),
                saveEventToDb(eventInfo_2),
                saveEventToDb(eventInfo_3)
            ]
            assert len(createdEvents) == 3
            assert eventInfo_1['seriesId'] == 1
            assert eventInfo_2['seriesId'] == 1
            assert eventInfo_3['seriesId'] == 1
            assert eventInfo_1['isRepeating'] == 1
            assert eventInfo_2['isRepeating'] == 1
            assert eventInfo_3['isRepeating'] == 1

            transaction.rollback()

@pytest.mark.integration
def test_saveEventToDb_multipleOffering():
    with mainDB.atomic() as transaction:
        with app.app_context():
            eventInfo_1 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': False, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate':'', 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}
            
            eventInfo_2 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': False, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate':'', 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}
            
            eventInfo_3 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': False, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate':'', 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}

            eventInfo_1['valid'] = True
            eventInfo_2['valid'] = True
            eventInfo_3['valid'] = True
            eventInfo_1['program'] = Program.get_by_id(1)
            eventInfo_2['program'] = Program.get_by_id(1)
            eventInfo_3['program'] = Program.get_by_id(1)

            g.current_user = User.get_by_id("ramsayb2")
            createdEvents = [
                saveEventToDb(eventInfo_1),
                saveEventToDb(eventInfo_2),
                saveEventToDb(eventInfo_3)
            ]
            assert len(createdEvents) == 3
            assert eventInfo_1['seriesId'] == 1
            assert eventInfo_2['seriesId'] == 1
            assert eventInfo_3['seriesId'] == 1
            assert eventInfo_1['isRepeating'] == 0
            assert eventInfo_2['isRepeating'] == 0
            assert eventInfo_3['isRepeating'] == 0

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
                        "id": eventId,
                        "program": 1,
                        "term": 1,
                        "name": "First Meetup",
                        "description": "This is a Test",
                        "timeStart": "06:00 PM",
                        "timeEnd": "09:00 PM",
                        "certRequirement": 9,
                        "location": "House",
                        'isFoodProvided': False,
                        'isRepeating': True,
                        'seriesId': 3,
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
        assert afterUpdate.seriesId is None
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
        # creates non repeating event
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
                                    endDate = " ",
                                    seriesId = None,
                                    program = 9)

        testingEvent = Event.get(Event.name == "Testing delete event")
        eventId = testingEvent.id

        # tests deletion of standard event
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEvent(eventId)
            event = Event.get_or_none(Event.id == eventId) 
        assert event is not None and event.isDeleted

        transaction.rollback()

        # create repeating events
        event_1 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': True, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate': parser.parse('12-12-2021'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring Week 1','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}
            
        event_2 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': True, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate': parser.parse('12-12-2021'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring Week 2','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}
            
        event_3 =  {'isFoodProvided': False, 'isRsvpRequired':False, 'rsvpLimit': None, 'isService':False, 'isAllVolunteerTraining': True,
                          'isTraining':True, 'isRepeating': True, 'seriesId':1, 'startDate': parser.parse('12-12-2021'),
                           'endDate': parser.parse('12-12-2021'), 'location':"this is only a test",
                           'timeEnd':'09:00 PM', 'timeStart':'06:00 PM', 'description':"Empty Bowls Spring 2021",
                           'name':'Empty Bowls Spring Week 3','term':1,'contactName':"Brianblius Ramsablius", 'contactEmail': 'ramsayBlius@gmail.com'}

        event_1['valid'] = True
        event_2['valid'] = True
        event_3['valid'] = True
        event_1['program'] = Program.get_by_id(1)
        event_2['program'] = Program.get_by_id(1)
        event_3['program'] = Program.get_by_id(1)
        createdEvents = [
                saveEventToDb(event_1),
                saveEventToDb(event_2),
                saveEventToDb(event_3)
            ]
        event = Event.get_by_id(createdEvents[0])
        seriesId = event.seriesId

        # check how many events exist before event deletion and isDeleted should be false since they are not deleted yet
        recurringEventsBefore = list(Event.select().where((Event.seriesId==seriesId)&(Event.deletionDate == None)).order_by(Event.seriesId))
        for counter, recurring in enumerate(recurringEventsBefore):
            assert recurring.name == ("Empty Bowls Spring Week " + str(counter + 1))
            assert recurring.isDeleted == False

        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEvent(createdEvents[0])
            event = Event.get_or_none(Event.id == createdEvents[0]) 
            assert event.isDeleted

        # check how many events exist after event deletion
        # event that got deleted now have a deletion date which is not None
        recurringEventsAfter = list(Event.select().where((Event.seriesId==seriesId)&(Event.deletionDate == None)).order_by(Event.seriesId))
        for counter, recurring in enumerate(recurringEventsAfter):
            assert recurring.name == ("Empty Bowls Spring Week " + str(counter + 1))
        assert (len(recurringEventsBefore)-1) == len(recurringEventsAfter)
        transaction.rollback()

        #creating recurring event again to test deleteEventandAll
        event_1['valid'] = True
        event_2['valid'] = True
        event_3['valid'] = True
        event_1['program'] = Program.get_by_id(1)
        event_2['program'] = Program.get_by_id(1)
        event_3['program'] = Program.get_by_id(1)
        createdEvents = [
                saveEventToDb(event_1),
                saveEventToDb(event_2),
                saveEventToDb(event_3)
            ]
        eventIdToDelete = Event.get_by_id(createdEvents[2])
        seriesId = event.seriesId

        totalRecurringEvents = len(Event.select().where(Event.seriesId == seriesId))
        #checks the number of all recurring events that will take place after a recurring event plus the event itself.
        eventPlusAllRecurringEventsAfter = len(Event.select().where((Event.seriesId == seriesId) & (Event.startDate >= eventIdToDelete.startDate)))
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteEventAndAllFollowing(eventIdToDelete)
            totalRecurringEventsAfter = len(Event.select().where((Event.seriesId == seriesId)&(Event.deletionDate == None)))
        assert (totalRecurringEvents - eventPlusAllRecurringEventsAfter) == totalRecurringEventsAfter
        transaction.rollback()
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            deleteAllEventsInSeries(eventIdToDelete)
            newTotalRecurringEvents = len(Event.select().where((Event.seriesId == seriesId)& (Event.startDate >= eventIdToDelete.startDate)))
        assert newTotalRecurringEvents == 0
        transaction.rollback()


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
        
        programForMultiple = Program.create(id = 16,
                                        programName = "TestMultiple",
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
                                         seriesId = 1,
                                         program= programForInterest)

        newRecurringSecond = Event.create(name = "Recurring second event",
                                          term = 2,
                                          description = "Test upcoming program event.",
                                          location = "The sun",
                                          startDate = date(2021,12,14),
                                          endDate = date(2021,12,15),
                                          seriesId = 1,
                                          program= programForInterest)

        newRecurringDifferentId = Event.create(name = "Recurring different Id",
                                               term = 2,
                                               description = "Test upcoming program event.",
                                               location = "The sun",
                                               startDate = date(2021,12,13),
                                               endDate = date(2021,12,13),
                                               seriesId = 2,
                                               program= programForInterest)
        
        multipleOfferingEvent = Event.create(name = "Multiple Offering Id",
                                            term = 2,
                                            description = "Test multiple offering event",
                                            location = "The moon",
                                            startDate = date(2021,12,13),
                                            endDate = date(2021,12,13),
                                            seriesId = 2,
                                            program= programForMultiple)

        # User has not RSVPd and is Interested
        addUserInterest(programForInterest.id, user)
        addUserInterest(programForInterest2.id, user)
        addUserInterest(programForBanning.id, user)
        addUserInterest(programForMultiple.id, user)
        eventsInUserInterestedProgram = getUpcomingEventsForUser(user, asOf = testDate)

        assert newProgramEvent in eventsInUserInterestedProgram
        assert newRecurringDifferentId in eventsInUserInterestedProgram
        assert newRecurringEvent in eventsInUserInterestedProgram
        assert newRecurringSecond not in eventsInUserInterestedProgram
        assert multipleOfferingEvent in eventsInUserInterestedProgram

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
        removeUserInterest(programForMultiple.id, user)

        eventsInUserRsvp = getUpcomingEventsForUser(user, asOf = testDate)
        assert eventsInUserRsvp == [noProgram]

        # Get upcoming for specific program only
        # we would have multiples with interests in both programs, but we specify only one
        addUserInterest(programForInterest.id, user)
        addUserInterest(programForInterest2.id, user)
        addUserInterest(programForMultiple.id, user)

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
def test_calculateNewSeriesId():

    maxSeriesId = Event.select(fn.MAX(Event.seriesId)).scalar()
    if maxSeriesId == None:
        maxSeriesId = 1
    else:
        maxSeriesId += 1
    assert calculateNewSeriesId() == maxSeriesId

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
                                     seriesId = 3,
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
                                     seriesId = 3,
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
                                     seriesId = 3,
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

        val = getPreviousSeriesEventData(testingEvent3.seriesId)
        assert val[0].username == "neillz"
        assert val[1].username == "ramsayb2"
        assert val[2].username == "khatts"
        transaction.rollback()



@pytest.mark.integration
def test_getPreviousMultipleOfferingEventData():
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
                                     startDate = "2022-12-12",
                                     endDate = "2022-12-12",
                                     seriesId = 3,
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
                                     startDate = "2022-12-19",
                                     endDate = "2022-12-19",
                                     seriesId = 3,
                                     program = 9)

        EventParticipant.create(user = User.get_by_id("neillz"),
                                                      event = testingEvent1.id,
                                                      hoursEarned = None)
        EventParticipant.create(user = User.get_by_id("ramsayb2"),
                                                      event = testingEvent1.id,
                                                      hoursEarned = None)
        EventParticipant.create(user = User.get_by_id("khatts"),
                                                      event = testingEvent1.id,
                                                      hoursEarned = None)

        val = getPreviousSeriesEventData(testingEvent2.seriesId)
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

@pytest.mark.integration
def test_getCountdownToEvent():
    """
    This functions creates events that are different times away from the current time and tests
    the output of the getCountdown
    """
    # Define a multiple offering datetime representing the current time
    currentTime = datetime.strptime('1/1/2024 12:00 PM', '%m/%d/%Y %I:%M %p')
    def makeEventIn(*, timeDifference=None, **kwargs):
        """
        Takes in a datetime.relativedelta object or keyword argumentsand creates a 1 hour long event that starts
        at currentTime + deltatime
        """
        nonlocal currentTime
        if kwargs:
            timeDifference = relativedelta(**kwargs)
        eventStart = currentTime + timeDifference
        eventEnd = eventStart + relativedelta(hours=1)
        irrelevantEventData = {'name': 'testing', 'term': 1, 'description': '', 'location': '', 'program': 1}
        return Event.create(timeStart=eventStart.time(), startDate=eventStart.date(), timeEnd=eventEnd.time(), endDate=eventEnd.date(), **irrelevantEventData)
    
    def testCountdown(expectedOutput, *, timeDifference=None, **kwargs):
        """
        This function creates an event in the future (using either a relativeDelta object or kwargs)
        and the makeEventIn() function to assert that the countdown until that event is equal to
        the expectedOutput parameter.
        
        Rolls back the DB changes after the function exits
        """
        nonlocal currentTime
        with mainDB.atomic() as transaction:
            event = makeEventIn(timeDifference=timeDifference, **kwargs)
            countdown = getCountdownToEvent(event, currentDatetime=currentTime)
            assert countdown == expectedOutput
            transaction.rollback()

    # Years and months away
    testCountdown("2 years and 5 months", years=2, months=5, days=1)

    # Years away
    testCountdown("1 year", years=1)

    # Months and days away
    testCountdown("1 month and 7 days", months=1, days=7)

    # Months away
    testCountdown("3 months", months=3)

    # Days away
    # When an event is more than a day after the current time today w/o hours
    testCountdown("4 days", days=4)

    # Days and hours away pt. 1
    # When an event is more than 1 day away before the current time today
    testCountdown("3 days", days=2, hours=22)

    # Days and hours away pt. 2
    # When an event is more than a day after the current time today
    testCountdown("2 days and 3 hours", days=2, hours=3)

    # 1 day before the current time today
    testCountdown("Tomorrow", hours=23, minutes=30)

    # Hours and minutes away
    testCountdown("2 hours and 30 minutes", hours=2, minutes=30)

    # Hours away
    testCountdown("3 hours", hours=3)

    # Minutes away
    testCountdown("45 minutes", minutes=45)

    # Less than a minute away
    testCountdown("<1 minute", minutes=0, seconds=30)

    # Current event
    testCountdown("Happening now", minutes=-30)
    
    # Past event
    testCountdown("Already passed", days=-1)

@pytest.mark.integration
def test_copyRsvpToNewEvent():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = "heggens"


            priorEvent = Event.create(name = "Req and Limit",
                                    term = 2,
                                    description = "Event that requries RSVP and has an RSVP limit set.",
                                    timeStart = "6:00 pm",
                                    timeEnd = "9:00 pm",
                                    location = "The Moon",
                                    isRsvpRequired = 1,
                                    startDate = "2022-12-19",
                                    endDate = "2022-12-19",
                                    program = 9)
            
            priorEvent.save()
            EventRsvp.create(user = "neillz",
                             event = priorEvent).save()
            EventRsvp.create(user = "partont",
                             event = priorEvent).save()
            
            newEvent = Event.create(name = "Req and Limit",
                                     term = 2,
                                     description = "Event that requries RSVP and has an RSVP limit set.",
                                     timeStart = "6:00 pm",
                                     timeEnd = "9:00 pm",
                                     location = "The Moon",
                                     isRsvpRequired = 1,
                                     startDate = "2022-12-19",
                                     endDate = "2022-12-19",
                                     program = 9)

            newEvent.save()
            assert len(EventRsvp.select().where(EventRsvp.event_id == priorEvent)) == 2
            assert len(EventRsvp.select().where(EventRsvp.event_id == newEvent)) == 0
            
            copyRsvpToNewEvent(model_to_dict(priorEvent), newEvent) 
            assert len(EventRsvp.select().where(EventRsvp.event_id == newEvent)) == 2

            transaction.rollback()

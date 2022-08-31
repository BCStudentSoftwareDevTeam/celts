from peewee import DoesNotExist, fn, JOIN
from dateutil import parser
from datetime import timedelta, date
import datetime
from werkzeug.datastructures import MultiDict
from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.eventRsvp import EventRsvp
from app.models.eventTemplate import EventTemplate
from app.models.programEvent import ProgramEvent
from app.models.eventFile import EventFile

from app.logic.adminLogs import createLog
from app.logic.utils import format24HourTime
from app.logic.fileHandler import FileHandler

def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return (Event.select(Event).join(ProgramEvent)
                    .where(ProgramEvent.program == program_id).distinct())
    else:
        return Event.select()

def deleteEvent(eventId):
    """
    Deletes an event, if it is a recurring event, rename all following events
    to make sure there is no gap in weeks.
    """
    event = Event.get_or_none(Event.id == eventId)
    program = event.singleProgram
    
    if event:
        if event.recurringId:
            recurringId = event.recurringId
            recurringEvents = list(Event.select().where(Event.recurringId==recurringId).order_by(Event.id)) # orders for tests
            eventDeleted = False

            # once the deleted event is detected, change all other names to the previous event's name
            for recurringEvent in recurringEvents:
                if eventDeleted:
                    Event.update({Event.name:newEventName}).where(Event.id==recurringEvent.id).execute()
                    newEventName = recurringEvent.name

                if recurringEvent == event:
                    newEventName = recurringEvent.name
                    eventDeleted = True

        event.delete_instance(recursive = True, delete_nullable = True)

        createLog(f"Deleted \"{event.name}\" for {program.programName}, which had a start date of {datetime.datetime.strftime(event.startDate, '%m/%d/%Y')}")

def attemptSaveEvent(eventData, attachmentFiles = None):
    newEventData = preprocessEventData(eventData)
    addfile= FileHandler(attachmentFiles)
    isValid, validationErrorMessage = validateNewEventData(newEventData)

    if not isValid:
        return False, validationErrorMessage

    try:
        events = saveEventToDb(newEventData)
        if  attachmentFiles:
            for event in events:
                addfile.saveFilesForEvent(event.id)
        return True, ""
    except Exception as e:
        print(e)
        return False, e

def saveEventToDb(newEventData):

    if not newEventData.get('valid', False):
        raise Exception("Unvalidated data passed to saveEventToDb")

    isNewEvent = ('id' not in newEventData)

    eventsToCreate = []
    recurringSeriesId = None
    if isNewEvent and newEventData['isRecurring']:
        eventsToCreate = calculateRecurringEventFrequency(newEventData)
        recurringSeriesId = calculateNewrecurringId()
    else:
        eventsToCreate.append({'name': f"{newEventData['name']}",
                                'date':newEventData['startDate'],
                                "week":1})
    eventRecords = []
    for eventInstance in eventsToCreate:
        with mainDB.atomic():
            eventData = {
                    "term": newEventData['term'],
                    "name": eventInstance['name'],
                    "description": newEventData['description'],
                    "timeStart": newEventData['timeStart'],
                    "timeEnd": newEventData['timeEnd'],
                    "location": newEventData['location'],
                    "recurringId": recurringSeriesId,
                    "isTraining": newEventData['isTraining'],
                    "isRsvpRequired": newEventData['isRsvpRequired'],
                    "isService": newEventData['isService'],
                    "startDate": eventInstance['date'],
                    "isAllVolunteerTraining": newEventData['isAllVolunteerTraining'],
                    "endDate": eventInstance['date'],
                    "contactEmail": newEventData['contactEmail'],
                    "contactName": newEventData['contactName']
            }

            # Create or update the event
            if isNewEvent:
                eventRecord = Event.create(**eventData)
                # TODO handle multiple programs
                if 'program' in newEventData:
                    ProgramEvent.create(program=newEventData['program'], event=eventRecord)
            else:
                eventRecord = Event.get_by_id(newEventData['id'])
                Event.update(**eventData).where(Event.id == eventRecord).execute()


            eventRecords.append(eventRecord)

    return eventRecords

def getStudentLedEvents(term):

    studentLedEvents = list(Event.select(Event, Program, ProgramEvent)
                             .join(ProgramEvent, attr = 'programEvent')
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == term).execute())
    programs = {}

    for event in studentLedEvents:
        programs.setdefault(event.programEvent.program, []).append(event)

    return programs

def getTrainingEvents(term, user):
    """
        The allTrainingsEvent query is designed to select and count eventId's after grouping them
        together by id's of similiar value. The query will then return the event that is associated
        with the most programs (highest count) by doing this we can ensure that the event being
        returned is the All Trainings Event.
        term: expected to be the ID of a term
        user: expected to be the current user
        return: a list of all trainings the user can view
    """
    trainingQuery = (Event.select(Event)
                           .join(ProgramEvent)
                           .join(Program)
                           .order_by(Event.isAllVolunteerTraining.desc(), Event.startDate)
                           .where(Event.isTraining, Event.term == term))
    hideBonner = (not user.isAdmin) and not (user.isStudent and user.isBonnerScholar)
    if hideBonner:
        trainingQuery = trainingQuery.where(Program.isBonnerScholars == False)

    return list(trainingQuery.distinct().execute())

def getBonnerEvents(term):

    bonnerScholarsEvents = list(Event.select(Event,ProgramEvent, Program.id.alias("program_id"))
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == term).execute())
    return bonnerScholarsEvents

def getOtherEvents(term):
    """
    Get the list of the events not caught by other functions to be displayed in
    the Other Events section of the Events List page.
    :return: A list of Other Event objects
    """
    # Gets all events that are not associated with a program and are not trainings
    # Gets all events that have a program but don't fit anywhere
    otherEvents = list(Event.select(Event, Program)
                        .join(ProgramEvent, JOIN.LEFT_OUTER)
                        .join(Program, JOIN.LEFT_OUTER)
                        .where(Event.term == term,
                               Event.isTraining == False,
                               Event.isAllVolunteerTraining == False,
                               ((ProgramEvent.program == None) |
                                ((Program.isStudentLed == False) &
                                (Program.isBonnerScholars == False))))
                        .order_by(Event.id).execute()
                      )

    return otherEvents

def getUpcomingEventsForUser(user, asOf=datetime.datetime.now()):
    """
        Get the list of upcoming events that the user is interested in.
        :param user: a username or User object
        :param asOf: The date to use when determining future and past events.
                      Used in testing, defaults to the current timestamp.
        :return: A list of Event objects
    """

    events =  list(Event.select()
                    .join(ProgramEvent, JOIN.LEFT_OUTER)
                    .join(Interest, JOIN.LEFT_OUTER, on=(ProgramEvent.program == Interest.program))
                    .join(EventRsvp, JOIN.LEFT_OUTER, on=(Event.id == EventRsvp.event))
                    .where(Event.startDate >= asOf,
                           (Interest.user == user) | (EventRsvp.user == user))
                    .distinct() # necessary because of multiple programs
                    .order_by(Event.startDate, Event.name).execute() # keeps the order of events the same when the dates are the same
                    )

    return events

def getParticipatedEventsForUser(user):
    """
        Get all the events a user has participated in.
        :param user: a username or User object
        :param asOf: The date to use when determining future and past events.
                      Used in testing, defaults to the current timestamp.
        :return: A list of Event objects
    """

    participatedEvents = (Event.select(Event, Program.programName)
                               .join(ProgramEvent, JOIN.LEFT_OUTER)
                               .join(Program, JOIN.LEFT_OUTER).switch()
                               .join(EventParticipant)
                               .where(EventParticipant.user == user,
                                      Event.isAllVolunteerTraining == False)
                               .order_by(Event.startDate, Event.name))

    allVolunteer = (Event.select(Event, "").join(EventParticipant).where(Event.isAllVolunteerTraining == True, EventParticipant.user == user))
    union = participatedEvents.union_all(allVolunteer)
    unionParticipationWithVolunteer = list(union.select_from(union.c.id, union.c.programName, union.c.startDate, union.c.name).order_by(union.c.startDate, union.c.name).execute())

    return unionParticipationWithVolunteer

def validateNewEventData(data):
    """
        Confirm that the provided data is valid for an event.

        Assumes the event data has been processed with `preprocessEventData`. NOT raw form data

        Returns 3 values: (boolean success, the validation error message, the data object)
    """

    if 'on' in [data['isRsvpRequired'], data['isTraining'], data['isService'], data['isRecurring']]:
        return (False, "Raw form data passed to validate method. Preprocess first.")

    if data['isRecurring'] and data['endDate']  <  data['startDate']:
        return (False, "Event start date is after event end date")

    if data['endDate'] ==  data['startDate'] and data['timeEnd'] <= data['timeStart']:
        return (False, "Event start time is after event end time")

    # Validation if we are inserting a new event
    if 'id' not in data:
        # Check for a pre-existing event with Event name, Description and Event Start date
        event = Event.select().where((Event.name == data['name']) &
                                 (Event.description == data['description']) &
                                 (Event.startDate == data['startDate']))

        try:
            Term.get_by_id(data['term'])
        except DoesNotExist as e:
            return (False, f"Not a valid term: {data['term']}")

        if event.exists():
            return (False, "This event already exists")

    data['valid'] = True
    return (True, "All inputs are valid.")

def calculateNewrecurringId():
    """
    Gets the highest recurring Id so that a new recurring Id can be assigned
    """
    recurringId = Event.select(fn.MAX(Event.recurringId)).scalar()
    if recurringId:
        return recurringId + 1
    else:
        return 1

def getPreviousRecurringEventData(recurringId):
    """
    Joins the User db table and Event Participant db table so that we can get the information of a participant if they attended an event
    """
    previousEventVolunteers = User.select(User).join(EventParticipant).join(Event).where(Event.recurringId==recurringId).distinct()
    return previousEventVolunteers

def calculateRecurringEventFrequency(event):
    """
        Calculate the events to create based on a recurring event start and end date. Takes a
        dictionary of event data.

        Assumes that the data has been processed with `preprocessEventData`. NOT raw form data.

        Return a list of events to create from the event data.
    """
    if not isinstance(event['endDate'], datetime.date) or not isinstance(event['startDate'], datetime.date):
        raise Exception("startDate and endDate must be datetime.date objects.")

    if event['endDate'] == event['startDate']:
        raise Exception("This event is not a recurring event")
    return [ {'name': f"{event['name']} Week {counter+1}",
              'date': event['startDate'] + datetime.timedelta(days=7*counter),
              "week": counter+1}
            for counter in range(0, ((event['endDate']-event['startDate']).days//7)+1)]

def preprocessEventData(eventData):
    """
        Ensures that the event data dictionary is consistent before it reaches the template or event logic.

        - dates should exist and be date objects if there is a value
        - checkbaxes should be True or False
        - if term is given, convert it to a model object
        - times should exist be strings in 24 hour format example: 14:40
    """
    ## Process checkboxes
    eventCheckBoxes = ['isRsvpRequired', 'isService', 'isTraining', 'isRecurring', 'isAllVolunteerTraining']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False
        else:
            eventData[checkBox] = bool(eventData[checkBox])

    ## Process dates
    eventDates = ['startDate', 'endDate']
    for date in eventDates:
        if date not in eventData:
            eventData[date] = ''
        elif type(eventData[date]) is str and eventData[date]:
            eventData[date] = parser.parse(eventData[date])
        elif not isinstance(eventData[date], datetime.date):
            eventData[date] = ''

    # If we aren't recurring, all of our events are single-day
    if not eventData['isRecurring']:
        eventData['endDate'] = eventData['startDate']

    # Process terms
    if 'term' in eventData:
        try:
            eventData['term'] = Term.get_by_id(eventData['term'])
        except DoesNotExist:
            eventData['term'] = ''

    if 'timeStart' in eventData:
        eventData['timeStart'] = format24HourTime(eventData['timeStart'])

    if 'timeEnd' in eventData:
        eventData['timeEnd'] = format24HourTime(eventData['timeEnd'])

    return eventData

def getTomorrowsEvents():
    """Grabs each event that occurs tomorrow"""
    tomorrowDate = date.today() + timedelta(days=1)
    events = list(Event.select().where(Event.startDate==tomorrowDate))
    return events

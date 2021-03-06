from peewee import DoesNotExist, fn, JOIN
from dateutil import parser
from datetime import timedelta, date
import datetime
from werkzeug.datastructures import MultiDict
from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.eventFacilitator import EventFacilitator
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.eventRsvp import EventRsvp
from app.models.eventTemplate import EventTemplate
from app.models.programEvent import ProgramEvent
from app.logic.adminLogs import createLog
from app.logic.utils import format24HourTime

def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return (Event.select(Event).join(ProgramEvent)
                    .where(ProgramEvent.program == program_id).distinct())
    else:
        return Event.select()

def deleteEvent(eventId):

    event = Event.get_or_none(Event.id == eventId)
    if event:
        event.delete_instance(recursive = True, delete_nullable = True)
        if event.startDate:
            createLog(f"Deleted event: {event.name}, which had a start date of {datetime.datetime.strftime(event.startDate, '%m/%d/%Y')}")

def attemptSaveEvent(eventData):

    newEventData = preprocessEventData(eventData)

    isValid, validationErrorMessage = validateNewEventData(newEventData)

    if not isValid:
        return False, validationErrorMessage

    try:
        events = saveEventToDb(newEventData)
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
                    "endDate": eventInstance['date']
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

            EventFacilitator.delete().where(EventFacilitator.event == eventRecord).execute()
            for f in newEventData['facilitators']:
                EventFacilitator.create(user=f, event=eventRecord)

            eventRecords.append(eventRecord)

    return eventRecords

def getStudentLedEvents(term):

    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == term))
    programs = {}

    for event in studentLedEvents.objects():
        programs.setdefault(Program.get_by_id(event.program_id), []).append(event)

    return programs

def getTrainingEvents(term):

    """
        The allTrainingsEvent query is designed to select and count eventId's after grouping them
        together by id's of similiar value. The query will then return the event that is associated
        with the most programs (highest count) by doing this we can ensure that the event being
        returned is the All Trainings Event.
    """
    try:
        allTrainingsEvent = ((ProgramEvent.select(ProgramEvent.event, fn.COUNT(1).alias('num_programs'))
                                            .join(Event)
                                            .group_by(ProgramEvent.event)
                                            .order_by(fn.COUNT(1).desc()))
                                            .where(Event.term == term).get())

        trainingEvents = (Event.select(Event)
    			               .order_by((Event.id == allTrainingsEvent.event.id).desc(), Event.startDate.desc())
                               .where(Event.isTraining,
                                      Event.term == term))

    except DoesNotExist:
        trainingEvents = (Event.select(Event)
    			               .order_by( Event.startDate.desc())
                               .where(Event.isTraining,
                                      Event.term == term))

    return list(trainingEvents)

def getBonnerEvents(term):

    bonnerScholarsEvents = (Event.select(Event, Program.id.alias("program_id"))
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == term))
    return list(bonnerScholarsEvents)

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
                            (Program.isStudentLed == False) &
                            (Program.isBonnerScholars == False)))
                    .order_by(Event.id)
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

    events = (Event.select()
                    .join(ProgramEvent, JOIN.LEFT_OUTER)
                    .join(Interest, JOIN.LEFT_OUTER, on=(ProgramEvent.program == Interest.program))
                    .join(EventRsvp, JOIN.LEFT_OUTER, on=(Event.id == EventRsvp.event))
                    .where(Event.startDate >= asOf,
                           (Interest.user == user) | (EventRsvp.user == user))
                    .distinct() # necessary because of multiple programs
                    .order_by(Event.startDate, Event.name) # keeps the order of events the same when the dates are the same
                    )

    return list(events)

def getAllFacilitators():
    facilitators = User.select(User).where((User.isFaculty == 1) | (User.isCeltsAdmin == 1) | (User.isCeltsStudentStaff == 1)).order_by(User.username) # ordered because of the tests
    return facilitators

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
    Joins the User db table and Event Participant db table so that we can get the information of a Particpant if they attended an event
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
        - facilitators should be a list of objects. Use the given list of usernames if possible
          (and check for a MultiDict with getlist), or else get it from the existing event
          (or use an empty list if no event)
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

    ## Get the facilitator objects from the list or from the event if there is a problem
    if 'facilitators' in eventData:
        eventData['facilitators'] = getFacilitatorsFromList(eventData['facilitators'])

    return eventData

def getFacilitatorsFromList(facilitatorList):
    """
    This function takes in a list of usernames or a string with the usernames of
        facilitators separated by commas (,) and returns a list of facilitator
        objects that match the usernames in the list
    facilitatorList: expected to be a list with facilitator usernames as strings
                        or a string of usernames separated by commas (,)
    return: list of facilitator objects matching the usernames in facilitatorList
    """
    if facilitatorList and type(facilitatorList) == str:
        facilitatorList = facilitatorList.split(',')
    # for each facilitator in facilitatorList, if it is not a blank string of null
    # add a user object matching said facilitator to finalFacilitatorList
    finalFacilitatorList = [User.get_by_id(facilitator) for facilitator in facilitatorList if facilitator]
    return finalFacilitatorList

def getTomorrowsEvents():
    """Grabs each event that occurs tomorrow"""
    tomorrowDate = date.today() + timedelta(days=1)
    events = list(Event.select().where(Event.startDate==tomorrowDate))
    return events

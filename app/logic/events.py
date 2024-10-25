from flask import  url_for, g, session
from peewee import DoesNotExist, fn, JOIN
from dateutil import parser
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
from werkzeug.datastructures import MultiDict
import json
from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.program import Program
from app.models.term import Term
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.eventRsvp import EventRsvp
from app.models.requirementMatch import RequirementMatch
from app.models.certificationRequirement import CertificationRequirement
from app.models.eventViews import EventView

from app.logic.createLogs import createActivityLog, createRsvpLog
from app.logic.utils import format24HourTime
from app.logic.fileHandler import FileHandler
from app.logic.certification import updateCertRequirementForEvent

def cancelEvent(eventId):
    """
    Cancels an event.
    """
    event = Event.get_or_none(Event.id == eventId)
    if event: 
        event.isCanceled = True
        event.save()

    program = event.program
    createActivityLog(f"Canceled <a href= \"{url_for('admin.eventDisplay', eventId = event.id)}\" >{event.name}</a> for {program.programName}, which had a start date of {datetime.strftime(event.startDate, '%m/%d/%Y')}.")


def deleteEvent(eventId):
    """
    Deletes an event, if it is a recurring event, rename all following events
    to make sure there is no gap in weeks.
    """
    event = Event.get_or_none(Event.id == eventId)

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

        program = event.program 

        if program:
            createActivityLog(f"Deleted \"{event.name}\" for {program.programName}, which had a start date of {datetime.strftime(event.startDate, '%m/%d/%Y')}.")
        else:
            createActivityLog(f"Deleted a non-program event, \"{event.name}\", which had a start date of {datetime.strftime(event.startDate, '%m/%d/%Y')}.")

        Event.update({Event.deletionDate: datetime.now(), Event.deletedBy: g.current_user}).where(Event.id == event.id).execute()


def deleteEventAndAllFollowing(eventId):
        """
        Deletes a recurring event and all the recurring events after it.
        Modified to also apply to the case of events with multiple offerings
        """
        event = Event.get_or_none(Event.id == eventId)
        if event:
            if event.recurringId:
                recurringId = event.recurringId
                recurringSeries = list(Event.select(Event.id).where((Event.recurringId == recurringId) & (Event.startDate >= event.startDate)))
                deletedEventList = [recurringEvent.id for recurringEvent in recurringSeries]                
                Event.update({Event.deletionDate: datetime.now(), Event.deletedBy: g.current_user}).where((Event.recurringId == recurringId) & (Event.startDate >= event.startDate)).execute()
                return deletedEventList

def deleteAllRecurringEvents(eventId):
        """
        Deletes all recurring events.
        Modified to also apply for events with multiple offerings
        """
        event = Event.get_or_none(Event.id == eventId)
        if event:
            if event.recurringId:
                recurringId = event.recurringId
            allRecurringEvents = list(Event.select(Event.id).where(Event.recurringId == recurringId).order_by(Event.startDate))
            eventId = allRecurringEvents[0].id
        return deleteEventAndAllFollowing(eventId)
        
def attemptSaveMultipleOfferings(eventData, attachmentFiles = None):
    """
    Tries to save an event with multiple offerings to the database:
    Creates separate event data inheriting from the original eventData
    with the specifics of each offering.
    Calls attemptSaveEvent on each of the newly created datum
    If any data is not valid it will return a validation error.

    Returns:
    allSavesWereSuccessful : bool | Whether or not all offering saves were successful
    savedOfferings : List[event] | A list of event objects holding all offerings that were saved. If allSavesWereSuccessful is False then this list will be empty.
    failedSavedOfferings : List[(int, str), ...] | Tuples containing the indicies of failed saved offerings and the associated validation error message. 
    """
    savedOfferings = []
    failedSavedOfferings = []
    allSavesWereSuccessful = True
    
    # Creates a shared multipleOfferingId for all offerings to have
    multipleOfferingId = calculateNewMultipleOfferingId()

    # Create separate event data inheriting from the original eventData
    multipleOfferingData = eventData.get('multipleOfferingData')
    with mainDB.atomic() as transaction:
        for index, event in enumerate(multipleOfferingData):
            multipleOfferingDict = eventData.copy()
            multipleOfferingDict.update({
                'name': event['eventName'],
                'startDate': event['eventDate'],
                'timeStart': event['startTime'],
                'timeEnd': event['endTime'],
                'multipleOfferingId': multipleOfferingId
                })
            # Try to save each offering
            savedEvents, validationErrorMessage = attemptSaveEvent(multipleOfferingDict, attachmentFiles)
            if validationErrorMessage:
                failedSavedOfferings.append((index, validationErrorMessage))
                allSavesWereSuccessful = False
            else:
                savedEvent = savedEvents[0]
                savedOfferings.append(savedEvent)
        if not allSavesWereSuccessful:
            savedOfferings = []
            transaction.rollback()

    return allSavesWereSuccessful, savedOfferings, failedSavedOfferings


def attemptSaveEvent(eventData, attachmentFiles = None, renewedEvent = False):
    """
    Tries to save an event to the database:
    Checks that the event data is valid and if it is, it continues to save the new
    event to the database and adds files if there are any.
    If it is not valid it will return a validation error.

    Returns:
    The saved event, created events and an error message if an error occurred.
    """

    # Manually set the value of RSVP Limit if it is and empty string since it is
    # automatically changed from "" to 0
    if eventData["rsvpLimit"] == "":
        eventData["rsvpLimit"] = None
        
    newEventData = preprocessEventData(eventData)
    
    isValid, validationErrorMessage = validateNewEventData(newEventData)
    if not isValid:
        return [], validationErrorMessage

    try:
        events = saveEventToDb(newEventData, renewedEvent)
        if attachmentFiles:
            for event in events:
                addFile = FileHandler(attachmentFiles, eventId=event.id)
                addFile.saveFiles(saveOriginalFile=events[0])
        return events, ""
    except Exception as e:
        print(f'Failed attemptSaveEvent() with Exception: {e}')
        return [], e

def saveEventToDb(newEventData, renewedEvent = False):
    
    if not newEventData.get('valid', False) and not renewedEvent:
        raise Exception("Unvalidated data passed to saveEventToDb")
    
    
    isNewEvent = ('id' not in newEventData)

    
    eventsToCreate = []
    recurringSeriesId = None
    multipleSeriesId = None
    if (isNewEvent and newEventData['isRecurring']) and not renewedEvent:
        eventsToCreate = getRecurringEventsData(newEventData)
        recurringSeriesId = calculateNewrecurringId()
        
    #temporarily applying the append for single events for now to tests  
    elif(isNewEvent and newEventData['isMultipleOffering']) and not renewedEvent:
        eventsToCreate.append({'name': f"{newEventData['name']}",
                                'date':newEventData['startDate'],
                                "week":1})
        multipleSeriesId = newEventData['multipleOfferingId']
        
    else:
        eventsToCreate.append({'name': f"{newEventData['name']}",
                                'date':newEventData['startDate'],
                                "week":1})
        if renewedEvent:
            recurringSeriesId = newEventData.get('recurringId')
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
                    "isFoodProvided" : newEventData['isFoodProvided'],
                    "isTraining": newEventData['isTraining'],
                    "isEngagement": newEventData['isEngagement'],
                    "isRsvpRequired": newEventData['isRsvpRequired'],
                    "isService": newEventData['isService'],
                    "startDate": eventInstance['date'],
                    "rsvpLimit": newEventData['rsvpLimit'],
                    "endDate": eventInstance['date'],
                    "contactEmail": newEventData['contactEmail'],
                    "contactName": newEventData['contactName']
                }

            # The three fields below are only relevant during event creation so we only set/change them when 
            # it is a new event. 
            if isNewEvent:
                eventData['program'] = newEventData['program']
                eventData['recurringId'] = recurringSeriesId
                eventData['multipleOfferingId'] = multipleSeriesId
                eventData["isAllVolunteerTraining"] = newEventData['isAllVolunteerTraining']
                eventRecord = Event.create(**eventData)
            else:
                eventRecord = Event.get_by_id(newEventData['id'])
                Event.update(**eventData).where(Event.id == eventRecord).execute()

            if 'certRequirement' in newEventData and newEventData['certRequirement'] != "":
                updateCertRequirementForEvent(eventRecord, newEventData['certRequirement'])

            eventRecords.append(eventRecord)
    return eventRecords

def getStudentLedEvents(term):
    studentLedEvents = list(Event.select(Event, Program)
                                 .join(Program)
                                 .where(Program.isStudentLed,
                                        Event.term == term, Event.deletionDate == None)
                                 .order_by(Event.startDate, Event.timeStart)
                                 .execute())

    programs = {}

    for event in studentLedEvents:
        programs.setdefault(event.program, []).append(event)

    return programs

def getUpcomingStudentLedCount(term, currentTime):
    """
        Return a count of all upcoming events for each student led program.
    """
    
    upcomingCount = (Program.select(Program.id, fn.COUNT(Event.id).alias("eventCount"))
                            .join(Event, on=(Program.id == Event.program_id))
                            .where(Program.isStudentLed,
                                    Event.term == term, Event.deletionDate == None,
                                    (Event.endDate > currentTime) | ((Event.endDate == currentTime) & (Event.timeEnd >= currentTime)),
                                    Event.isCanceled == False)
                            .group_by(Program.id))
    
    programCountDict = {}

    for programCount in upcomingCount:
        programCountDict[programCount.id] = programCount.eventCount
    return programCountDict

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
    trainingQuery = (Event.select(Event).distinct()
                          .join(Program, JOIN.LEFT_OUTER)
                          .where(Event.isTraining == True,
                                 Event.term == term, Event.deletionDate == None)
                          .order_by(Event.isAllVolunteerTraining.desc(), Event.startDate, Event.timeStart))

    hideBonner = (not user.isAdmin) and not (user.isStudent and user.isBonnerScholar)
    if hideBonner:
        trainingQuery = trainingQuery.where(Program.isBonnerScholars == False)

    return list(trainingQuery.execute())

def getBonnerEvents(term):
    bonnerScholarsEvents = list(Event.select(Event, Program.id.alias("program_id"))
                                     .join(Program)
                                     .where(Program.isBonnerScholars,
                                            Event.term == term, Event.deletionDate == None)
                                     .order_by(Event.startDate, Event.timeStart)
                                     .execute())
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
                            .join(Program, JOIN.LEFT_OUTER)
                            .where(Event.term == term, Event.deletionDate == None,
                                   Event.isTraining == False,
                                   Event.isAllVolunteerTraining == False,
                                   ((Program.isOtherCeltsSponsored) |
                                   ((Program.isStudentLed == False) &
                                   (Program.isBonnerScholars == False))))
                            .order_by(Event.startDate, Event.timeStart, Event.id)
                            .execute())

    return otherEvents

def getUpcomingEventsForUser(user, asOf=datetime.now(), program=None):
    """
        Get the list of upcoming events that the user is interested in as long
        as they are not banned from the program that the event is a part of.
        :param user: a username or User object
        :param asOf: The date to use when determining future and past events.
                      Used in testing, defaults to the current timestamp.
        :return: A list of Event objects
    """

    events =  (Event.select().distinct()
                    .join(ProgramBan, JOIN.LEFT_OUTER, on=((ProgramBan.program == Event.program) & (ProgramBan.user == user)))
                    .join(Interest, JOIN.LEFT_OUTER, on=(Event.program == Interest.program))
                    .join(EventRsvp, JOIN.LEFT_OUTER, on=(Event.id == EventRsvp.event))
                    .where(Event.deletionDate == None, Event.startDate >= asOf,
                          (Interest.user == user) | (EventRsvp.user == user),
                          ProgramBan.user.is_null(True) | (ProgramBan.endDate < asOf)))

    if program:
        events = events.where(Event.program == program)

    events = events.order_by(Event.startDate, Event.timeStart)

    eventsList = []
    shownRecurringEventList = []
    shownMultipleOfferingEventList = []

    # removes all recurring events except for the next upcoming one
    for event in events:
        if event.recurringId or event.multipleOfferingId:
            if not event.isCanceled:
                if event.recurringId not in shownRecurringEventList:
                    eventsList.append(event)
                    shownRecurringEventList.append(event.recurringId)
                if event.multipleOfferingId not in shownMultipleOfferingEventList:
                    eventsList.append(event)
                    shownMultipleOfferingEventList.append(event.multipleOfferingId)
        else:
            if not event.isCanceled:
                eventsList.append(event)

    return eventsList

def getParticipatedEventsForUser(user):
    """
        Get all the events a user has participated in.
        :param user: a username or User object
        :param asOf: The date to use when determining future and past events.
                      Used in testing, defaults to the current timestamp.
        :return: A list of Event objects
    """

    participatedEvents = (Event.select(Event, Program.programName)
                               .join(Program, JOIN.LEFT_OUTER).switch()
                               .join(EventParticipant)
                               .where(EventParticipant.user == user,
                                      Event.isAllVolunteerTraining == False)
                               .order_by(Event.startDate, Event.name))

    allVolunteer = (Event.select(Event, "")
                         .join(EventParticipant)
                         .where(Event.isAllVolunteerTraining == True,
                                EventParticipant.user == user))
    union = participatedEvents.union_all(allVolunteer)
    unionParticipationWithVolunteer = list(union.select_from(union.c.id, union.c.programName, union.c.startDate, union.c.name).order_by(union.c.startDate, union.c.name).execute())

    return unionParticipationWithVolunteer

def validateNewEventData(data):
    """
        Confirm that the provided data is valid for an event.

        Assumes the event data has been processed with `preprocessEventData`. NOT raw form data

        Returns 3 values: (boolean success, the validation error message, the data object)
    """

    if 'on' in [data['isFoodProvided'], data['isRsvpRequired'], data['isTraining'], data['isEngagement'], data['isService'], data['isRecurring'], data['isMultipleOffering']]:
        return (False, "Raw form data passed to validate method. Preprocess first.")

    if data['isRecurring'] and data['endDate']  <  data['startDate']:
        return (False, "Event start date is after event end date.")

    if data['timeEnd'] <= data['timeStart']:
        return (False, "Event end time must be after start time.")
    
    # Validation if we are inserting a new event
    if 'id' not in data:

        sameEventList = list((Event.select().where((Event.name == data['name']) &
                                                   (Event.location == data['location']) &
                                                   (Event.startDate == data['startDate']) &
                                                   (Event.timeStart == data['timeStart'])).execute()))
        
        sameEventListCopy = sameEventList.copy()

        for event in sameEventListCopy:
            if event.isCanceled or event.recurringId:   
                sameEventList.remove(event)

        try:
            Term.get_by_id(data['term'])
        except DoesNotExist as e:
            return (False, f"Not a valid term: {data['term']}")
        if sameEventList:
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
def calculateNewMultipleOfferingId():
    """
    Gets the highest recurring Id so that a new recurring Id can be assigned
    """
    multipleOfferingId = Event.select(fn.MAX(Event.multipleOfferingId)).scalar()
    if multipleOfferingId:
        return multipleOfferingId + 1
    else:
        return 1

def getPreviousRecurringEventData(recurringId):
    """
    Joins the User db table and Event Participant db table so that we can get the information of a participant if they attended an event
    """
    previousEventVolunteers = (User.select(User).distinct()
                                   .join(EventParticipant)
                                   .join(Event)
                                   .where(Event.recurringId==recurringId))
    return previousEventVolunteers

def getPreviousMultipleOfferingEventData(multipleOfferingId):
    """
    Joins the User db table and Event Participant db table so that we can get the information of a participant if they attended an event
    """
    previousEventVolunteers = (User.select(User).distinct()
                                   .join(EventParticipant)
                                   .join(Event)
                                   .where(Event.multipleOfferingId == multipleOfferingId))
    return previousEventVolunteers

def getRecurringEventsData(eventData):
    """
        Calculate the events to create based on a recurring event start and end date. Takes a
        dictionary of event data.

        Assumes that the data has been processed with `preprocessEventData`. NOT raw form data.

        Return a list of events to create from the event data.
    """
    if not isinstance(eventData['endDate'], date) or not isinstance(eventData['startDate'], date):
        raise Exception("startDate and endDate must be datetime.date objects.")

    if eventData['endDate'] == eventData['startDate']:
        raise Exception("This event is not a recurring event")
    
    return [ {'name': f"{eventData['name']} Week {counter+1}",
              'date': eventData['startDate'] + timedelta(days=7*counter),
              "week": counter+1}
            for counter in range(0, ((eventData['endDate']-eventData['startDate']).days//7)+1)]

def preprocessEventData(eventData):
    """
        Ensures that the event data dictionary is consistent before it reaches the template or event logic.

        - dates should exist and be date objects if there is a value
        - checkboxes should be True or False
        - if term is given, convert it to a model object
        - times should exist be strings in 24 hour format example: 14:40
        - multipleOfferingData should be a JSON string
        - Look up matching certification requirement if necessary
    """
    ## Process checkboxes
    eventCheckBoxes = ['isFoodProvided', 'isRsvpRequired', 'isService', 'isTraining', 'isEngagement', 'isRecurring', 'isMultipleOffering', 'isAllVolunteerTraining']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False
        else:
            eventData[checkBox] = bool(eventData[checkBox])

    ## Process dates
    eventDates = ['startDate', 'endDate']
    for eventDate in eventDates:
        if eventDate not in eventData:  # There is no date given
            eventData[eventDate] = ''
        elif type(eventData[eventDate]) is str and eventData[eventDate]:  # The date is a nonempty string 
            eventData[eventDate] = parser.parse(eventData[eventDate])
        elif not isinstance(eventData[eventDate], date):  # The date is not a date object
            eventData[eventDate] = ''
    
    # If we aren't recurring, all of our events are single-day or mutliple offerings, which also have the same start and end date
    if not eventData['isRecurring']:
        eventData['endDate'] = eventData['startDate']
    
    # Process multipleOfferingData
    if 'multipleOfferingData' not in eventData:
        eventData['multipleOfferingData'] = json.dumps([])
    elif type(eventData['multipleOfferingData']) is str:
        try:
            multipleOfferingData = json.loads(eventData['multipleOfferingData'])
            eventData['multipleOfferingData'] = multipleOfferingData
            if type(multipleOfferingData) != list:
                eventData['multipleOfferingData'] = json.dumps([])
        except json.decoder.JSONDecodeError as e:
            eventData['multipleOfferingData'] = json.dumps([])
    if type(eventData['multipleOfferingData']) is list:
        # validate the list data. Make sure there is 'eventName', 'startDate', 'timeStart', 'timeEnd', and 'isDuplicate' data
        multipleOfferingData = eventData['multipleOfferingData']
        for offeringDatum in multipleOfferingData:    
            for attribute in ['eventName', 'startDate', 'timeStart', 'timeEnd']:
                if type(offeringDatum.get(attribute)) != str:
                    offeringDatum[attribute] = ''
            if type(offeringDatum.get('isDuplicate')) != bool:
                    offeringDatum['isDuplicate'] = False

        eventData['multipleOfferingData'] = json.dumps(eventData['multipleOfferingData'])
    
    # Process terms
    if 'term' in eventData:
        try:
            eventData['term'] = Term.get_by_id(eventData['term'])
        except DoesNotExist:
            eventData['term'] = ''
    
    # Process requirement
    if 'certRequirement' in eventData:
        try:
            eventData['certRequirement'] = CertificationRequirement.get_by_id(eventData['certRequirement'])
        except DoesNotExist:
            eventData['certRequirement'] = ''
    elif 'id' in eventData:
        # look up requirement
        match = RequirementMatch.get_or_none(event=eventData['id'])
        if match:
            eventData['certRequirement'] = match.requirement
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

def addEventView(viewer,event):
    """This checks if the current user already viewed the event. If not, insert a recored to EventView table"""
    if not viewer.isCeltsAdmin:
         EventView.get_or_create(user = viewer, event = event)   

def getEventRsvpCountsForTerm(term):
    """
        Get all of the RSVPs for the events that exist in the term.
        Returns a dictionary with the event id as the key and the amount of
        current RSVPs to that event as the pair.
    """
    amount = (Event.select(Event, fn.COUNT(EventRsvp.event_id).alias('count'))
                   .join(EventRsvp, JOIN.LEFT_OUTER)
                   .where(Event.term == term, Event.deletionDate == None)
                   .group_by(Event.id))

    amountAsDict = {event.id: event.count for event in amount}

    return amountAsDict

def getEventRsvpCount(eventId):
    """
        Returns the number of RSVP'd participants for a given eventId.
    """
    return len(EventRsvp.select().where(EventRsvp.event_id == eventId))

def getCountdownToEvent(event, *, currentDatetime=None):
    """
    Given an event, this function returns a string that conveys the amount of time left
    until the start of the event.

    Note about dates:
    Natural language is unintuitive. There are two major rules that govern how we discuss dates.
    - If an event happens tomorrow but less than 24 hours away from us we still say that it happens 
    tomorrow with no mention of the hour. 
    - If an event happens tomorrow but more than 24 hours away from us, we'll count the number of days 
    and hours in actual time.

    E.g. if the current time of day is greater than the event start's time of day, we give a number of days 
    relative to this morning and exclude all hours and minutes

    On the other hand, if the current time of day is less or equal to the event's start of day we can produce 
    the real difference in days and hours without the aforementioned simplifying language.
    """

    if currentDatetime is None:
        currentDatetime = datetime.now().replace(second=0, microsecond=0)  
    currentMorning = currentDatetime.replace(hour=0, minute=0)

    eventStart = datetime.combine(event.startDate, event.timeStart)
    eventEnd = datetime.combine(event.endDate, event.timeEnd)
    
    if eventEnd < currentDatetime:
        return "Already passed"
    elif eventStart <= currentDatetime <= eventEnd:
        return "Happening now"
    
    timeUntilEvent = relativedelta(eventStart, currentDatetime)
    calendarDelta = relativedelta(eventStart, currentMorning)
    calendarYearsUntilEvent = calendarDelta.years
    calendarMonthsUntilEvent = calendarDelta.months
    calendarDaysUntilEvent = calendarDelta.days

    yearString = f"{calendarYearsUntilEvent} year{'s' if calendarYearsUntilEvent > 1 else ''}"
    monthString = f"{calendarMonthsUntilEvent} month{'s' if calendarMonthsUntilEvent > 1 else ''}"
    dayString = f"{calendarDaysUntilEvent} day{'s' if calendarDaysUntilEvent > 1 else ''}"
    hourString = f"{timeUntilEvent.hours} hour{'s' if timeUntilEvent.hours > 1 else ''}"
    minuteString = f"{timeUntilEvent.minutes} minute{'s' if timeUntilEvent.minutes > 1 else ''}"
    
    # Years until
    if calendarYearsUntilEvent: 
        if calendarMonthsUntilEvent:
            return f"{yearString} and {monthString}"
        return f"{yearString}"
    # Months until
    if calendarMonthsUntilEvent:
        if calendarDaysUntilEvent:
            return f"{monthString} and {dayString}"
        return f"{monthString}"
    # Days until
    if calendarDaysUntilEvent:
        if eventStart.time() < currentDatetime.time():
            if calendarDaysUntilEvent == 1:
                return "Tomorrow"
            return f"{dayString}"
        if timeUntilEvent.hours:
            return f"{dayString} and {hourString}"
        return f"{dayString}"
    # Hours until
    if timeUntilEvent.hours:
        if timeUntilEvent.minutes:
            return f"{hourString} and {minuteString}"
        return f"{hourString}"
    # Minutes until
    elif timeUntilEvent.minutes > 1:
        return f"{minuteString}"
    # Seconds until
    return "<1 minute"
    
def copyRsvpToNewEvent(priorEvent, newEvent):
    """
        Copies rvsps from priorEvent to newEvent
    """
    rsvpInfo = list(EventRsvp.select().where(EventRsvp.event == priorEvent['id']).execute())
    
    for student in rsvpInfo:
        newRsvp = EventRsvp(
                user = student.user,
                event = newEvent,
                rsvpWaitlist = student.rsvpWaitlist
            )
        newRsvp.save()
    numRsvps = len(rsvpInfo)
    if numRsvps:
        createRsvpLog(newEvent, f"Copied {numRsvps} Rsvps from {priorEvent['name']} to {newEvent.name}")

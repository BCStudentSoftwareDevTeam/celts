from flask import  url_for
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
from app.models.term import Term
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.eventRsvp import EventRsvp
from app.models.requirementMatch import RequirementMatch
from app.models.certificationRequirement import CertificationRequirement
from app.models.eventViews import EventView

from app.logic.createLogs import createAdminLog
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
    createAdminLog(f"Canceled <a href= \"{url_for('admin.eventDisplay', eventId = event)}\" >{event.name}</a> for {program.programName}, which had a start date of {datetime.datetime.strftime(event.startDate, '%m/%d/%Y')}.")


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
            createAdminLog(f"Deleted \"{event.name}\" for {program.programName}, which had a start date of {datetime.datetime.strftime(event.startDate, '%m/%d/%Y')}.")
        else:
            createAdminLog(f"Deleted a non-program event, \"{event.name}\", which had a start date of {datetime.datetime.strftime(event.startDate, '%m/%d/%Y')}.")

        event.delete_instance(recursive = True, delete_nullable = True)

def deleteEventAndAllFollowing(eventId):
        """
        Deletes a recurring event and all the recurring events after it.
        """
        event = Event.get_or_none(Event.id == eventId)
        if event:
            if event.recurringId:
                recurringId = event.recurringId
                recurringSeries = list(Event.select().where((Event.recurringId == recurringId) & (Event.startDate >= event.startDate)))
        for seriesEvent in recurringSeries:
            seriesEvent.delete_instance(recursive = True)

def deleteAllRecurringEvents(eventId):
        """
        Deletes all recurring events.
        """
        event = Event.get_or_none(Event.id == eventId)
        if event:
            if event.recurringId:
                recurringId = event.recurringId
                allRecurringEvents = list(Event.select().where(Event.recurringId == recurringId))
            for aRecurringEvent in allRecurringEvents:
                aRecurringEvent.delete_instance(recursive = True)


def attemptSaveEvent(eventData, attachmentFiles = None):
    """
    Tries to save an event to the database:
    Checks that the event data is valid and if it is it continus to saves the new
    event to the database and adds files if there are any.
    If it is not valid it will return a validation error.

    Returns:
    Created events and an error message.
    """

    # Manually set the value of RSVP Limit if it is and empty string since it is
    # automatically changed from "" to 0
    if eventData["rsvpLimit"] == "":
        eventData["rsvpLimit"] = None
    newEventData = preprocessEventData(eventData)
    isValid, validationErrorMessage = validateNewEventData(newEventData)

    if not isValid:
        return False, validationErrorMessage

    try:
        events = saveEventToDb(newEventData)
        if attachmentFiles:
            for event in events:
                addFile= FileHandler(attachmentFiles, eventId=event.id)
                addFile.saveFiles(saveOriginalFile=events[0])

        return events, " "
    except Exception as e:
        print(f'Failed attemptSaveEvent() with Exception:{e}')
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
                    "isFoodProvided" : newEventData['isFoodProvided'],
                    "isTraining": newEventData['isTraining'],
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
                                        Event.term == term)
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
                                    Event.term == term,
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
                                 Event.term == term)
                          .order_by(Event.isAllVolunteerTraining.desc(), Event.startDate, Event.timeStart))

    hideBonner = (not user.isAdmin) and not (user.isStudent and user.isBonnerScholar)
    if hideBonner:
        trainingQuery = trainingQuery.where(Program.isBonnerScholars == False)

    return list(trainingQuery.execute())

def getBonnerEvents(term):
    bonnerScholarsEvents = list(Event.select(Event, Program.id.alias("program_id"))
                                     .join(Program)
                                     .where(Program.isBonnerScholars,
                                            Event.term == term)
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
                            .where(Event.term == term,
                                   Event.isTraining == False,
                                   Event.isAllVolunteerTraining == False,
                                   ((Program.isOtherCeltsSponsored) |
                                   ((Program.isStudentLed == False) &
                                   (Program.isBonnerScholars == False))))
                            .order_by(Event.startDate, Event.timeStart, Event.id)
                            .execute())

    return otherEvents

def getUpcomingEventsForUser(user, asOf=datetime.datetime.now(), program=None):
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
                    .where(Event.startDate >= asOf,
                          (Interest.user == user) | (EventRsvp.user == user),
                          ProgramBan.user.is_null(True) | (ProgramBan.endDate < asOf)))

    if program:
        events = events.where(Event.program == program)

    events = events.order_by(Event.startDate, Event.name)

    events_list = []
    shown_recurring_event_list = []

    # removes all recurring events except for the next upcoming one
    for event in events:
        if event.recurringId:
            if not event.isCanceled:
                if event.recurringId not in shown_recurring_event_list:
                    events_list.append(event)
                    shown_recurring_event_list.append(event.recurringId)
        else:
            if not event.isCanceled:
                events_list.append(event)

    return events_list

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

    if 'on' in [data['isFoodProvided'], data['isRsvpRequired'], data['isTraining'], data['isService'], data['isRecurring']]:
        return (False, "Raw form data passed to validate method. Preprocess first.")

    if data['isRecurring'] and data['endDate']  <  data['startDate']:
        return (False, "Event start date is after event end date.")

    if data['timeEnd'] <= data['timeStart']:
        return (False, "Event end time must be after start time.")

    # Validation if we are inserting a new event
    if 'id' not in data:

        event = (Event.select()
                      .where((Event.name == data['name']) &
                             (Event.location == data['location']) &
                             (Event.startDate == data['startDate']) &
                             (Event.timeStart == data['timeStart'])))

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
    previousEventVolunteers = (User.select(User).distinct()
                                   .join(EventParticipant)
                                   .join(Event)
                                   .where(Event.recurringId==recurringId))
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
        - checkboxes should be True or False
        - if term is given, convert it to a model object
        - times should exist be strings in 24 hour format example: 14:40
        - Look up matching certification requirement if necessary
    """
    ## Process checkboxes
    eventCheckBoxes = ['isFoodProvided', 'isRsvpRequired', 'isService', 'isTraining', 'isRecurring', 'isAllVolunteerTraining']

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
                   .where(Event.term == term)
                   .group_by(Event.id))

    amountAsDict = {event.id: event.count for event in amount}

    return amountAsDict

def getEventRsvpCount(eventId):
    """
        Returns the number of RSVP'd participants for a given eventId.
    """
    return len(EventRsvp.select().where(EventRsvp.event_id == eventId))

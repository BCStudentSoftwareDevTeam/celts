from peewee import DoesNotExist
from datetime import date, datetime, time
from dateutil import parser

from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.models.interest import Interest
from app.models.facilitator import Facilitator
from app.models.program import Program
from app.models.term import Term
from app.models.eventTemplate import EventTemplate
from app.models.programEvent import ProgramEvent
from app.logic.eventCreation import setValueForUncheckedBox, calculateRecurringEventFrequency, validateNewEventData

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

def attemptSaveEvent(eventData):

    newEventData = setValueForUncheckedBox(eventData)

    #if an event is not recurring then it will have same end and start date
    if newEventData['endDate'] == '':
        newEventData['endDate'] = newEventData['startDate']

    dataIsValid, validationErrorMessage, newEventData = validateNewEventData(newEventData)

    if not dataIsValid:
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

    isNewEvent = ('eventId' not in newEventData)

    eventsToCreate = []
    if isNewEvent and newEventData['isRecurring'] == 'on':
        eventsToCreate = calculateRecurringEventFrequency(newEventData)
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
                    "isRecurring": newEventData['isRecurring'],
                    "isTraining": newEventData['isTraining'],
                    "isRsvpRequired": newEventData['isRsvpRequired'],
                    "isService": newEventData['isService'],
                    "startDate": parser.parse(eventInstance['date']),
                    "endDate": parser.parse(eventInstance['date'])
            }

            # Create or update the event
            if isNewEvent:
                eventRecord = Event.create(**eventData)
                # TODO handle multiple programs
                if 'program' in newEventData:
                    ProgramEvent.create(program=newEventData['program'], event=eventRecord)
            else:
                eventData['id'] = newEventData['eventId']
                eventRecord = Event.update(**eventData).where(Event.id == eventData['id']).execute()

            Facilitator.delete().where(Facilitator.event == eventRecord).execute()
            #TODO handle multiple facilitators
            Facilitator.create(user=newEventData['eventFacilitator'], event=eventRecord)

            eventRecords.append(eventRecord)

    return eventRecords

def groupEventsByProgram(eventQuery):
    programs = {}

    for event in eventQuery.objects():
        programs.setdefault(Program.get_by_id(event.program_id), []).append(event)

    return programs

def groupEventsByCategory(term):

    term = Term.get_by_id(term)

    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == term))

    trainingEvents = (Event.select(Event, Program.id.alias("program_id"))
                           .join(ProgramEvent)
                           .join(Program)
                           .where(Event.isTraining,
                                  Event.term == term))


    bonnerScholarsEvents = (Event.select(Event, Program.id.alias("program_id"))
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == term))

    oneTimeEvents = (Event.select(Event, Program.id.alias("program_id"))
                          .join(ProgramEvent)
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False,
                                 Event.term == term))

    categorizedEvents = {"Student Led Events" : groupEventsByProgram(studentLedEvents),
                         "Trainings" : groupEventsByProgram(trainingEvents),
                         "Bonner Scholars" : groupEventsByProgram(bonnerScholarsEvents),
                         "One Time Events" : groupEventsByProgram(oneTimeEvents)}
    return categorizedEvents

def getUpcomingEventsForUser(user,asOf=datetime.now()):
    """
        Get the list of upcoming events that the user is interested in.

        :param user: a username or User object
        :param asOf: The date to use when determining future and past events.
                      Used in testing, defaults to the current timestamp.
        :return: A list of Event objects
    """

    events = (Event.select(Event)
                            .join(ProgramEvent)
                            .join(Interest, on=(ProgramEvent.program == Interest.program))
                            .where(Interest.user == user)
                            .where(Event.startDate >= asOf)
                            .where(Event.timeStart > asOf.time())
                            .distinct() # necessary because of multiple programs
                            .order_by(Event.startDate, Event.name) # keeps the order of events the same when the dates are the same
                            )
    return list(events)

def getAllFacilitators():

    facilitators = User.select(User).where((User.isFaculty == 1) | (User.isCeltsAdmin == 1) | (User.isCeltsStudentStaff == 1))
    return facilitators

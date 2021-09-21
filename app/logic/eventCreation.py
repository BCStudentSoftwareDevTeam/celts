from dateutil import parser
from datetime import *

from app.models import mainDB
from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator

def validateNewEventData(newEventData, checkExists=True):

    if parser.parse(newEventData['eventEndDate'])  <  parser.parse(newEventData['eventStartDate']):
        return (False, "Event start date is after event end date", newEventData)

    if parser.parse(newEventData['eventEndDate']) ==   parser.parse(newEventData['eventStartDate']) and newEventData['eventEndTime'] <=  newEventData['eventStartTime']:
        return (False, "Event start time is after event end time", newEventData)

    if newEventData['eventIsTraining'] == 'on' and newEventData['eventRequiredForProgram'] == False: #default value for checked button is on
        return (False, "A training event must be required for the program.", newEventData)

    if not newEventData['eventRSVP'] == 'on':
        if not isinstance(newEventData['eventRSVP'], bool):
            return (False, "Event RSVP must be a boolean", newEventData)

    if not newEventData['eventRequiredForProgram'] == 'on':
        if not isinstance(newEventData['eventRequiredForProgram'], bool):
            return (False, "Event Required must be a boolean", newEventData)

    if not newEventData['eventIsTraining'] == 'on':
        if not isinstance(newEventData['eventIsTraining'], bool):
            return (False, "Event Training must be a boolean", newEventData)


    if not newEventData['eventServiceHours'] == 'on':
        if not isinstance(newEventData['eventServiceHours'], bool):
            return (False, "Event Service Hours must be a boolean", newEventData)


    # Event name, Description and Event Start date
    event = Event.select().where((Event.name == newEventData['eventName']) &
                             (Event.description == newEventData['eventDescription']) &
                             (Event.startDate == parser.parse(newEventData['eventStartDate'])))

    if checkExists and event.exists():
        return (False, "This event already exists", newEventData)

    newEventData['valid'] = True
    return (True, "All inputs are valid.", newEventData)

def calculateRecurringEventFrequency(recurringEventInfo):
    """
    """

    eventName = recurringEventInfo['eventName']

    endDate = datetime.strptime(recurringEventInfo['eventEndDate'], '%m-%d-%Y')
    startDate = datetime.strptime(recurringEventInfo['eventStartDate'], '%m-%d-%Y')

    recurringEvents = []

    if endDate == startDate:
        raise Exception("This event is not a recurring Event")

    counter = 0
    for i in range(0, ((endDate-startDate).days +1), 7):
        counter += 1
        recurringEvents.append({'name': f"{eventName} Week {counter}",
                                'date':startDate.strftime('%m-%d-%Y'),
                                "week":counter})
        startDate += timedelta(days=7)

    return recurringEvents


def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining', 'eventIsRecurring']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData

def createNewEvent(newEventData):
    """
    Creates a new event and facilitator for that event
    The newEventData must have gone through the validateNewEventData function
    for 'valid' to be True.
    param: newEventData - dict with the event information
    """
    if newEventData['valid'] == True:
        # get the program first so if there's an exception we don't create the other stuff
        program = Program.get_by_id(newEventData['programId'])

        eventsToCreate = []
        if newEventData['eventIsRecurring'] == 'on':
            eventsToCreate = calculateRecurringEventFrequency(newEventData)
        else:
            eventsToCreate.append({'name': f"{newEventData['eventName']}",
                                    'date':newEventData['eventStartDate'],
                                    "week":1})

        for eventInstance in eventsToCreate:
            with mainDB.atomic():
                newEvent = Event.create(name = eventInstance['name'],
                                          term = newEventData['eventTerm'],
                                          description= newEventData['eventDescription'],
                                          timeStart = newEventData['eventStartTime'],
                                          timeEnd = newEventData['eventEndTime'],
                                          location = newEventData['eventLocation'],
                                          isRecurring = newEventData['eventIsRecurring'],
                                          isRsvpRequired = newEventData['eventRSVP'],
                                          isPrerequisiteForProgram = newEventData['eventRequiredForProgram'],
                                          isTraining = newEventData['eventIsTraining'],
                                          isService = newEventData['eventServiceHours'],
                                          startDate =  parser.parse(eventInstance['date']),
                                          endDate =  parser.parse(eventInstance['date']))

                programEvent = ProgramEvent.create(program=program, event=newEvent)

                facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],event = newEvent)

    else:
        raise Exception("Invalid Data")

    return newEvent


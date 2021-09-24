from dateutil import parser
from datetime import *

from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator

def validateNewEventData(newEventData):

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


    # Check for a pre-existing event with Event name, Description and Event Start date
    event = Event.select().where((Event.name == newEventData['eventName']) &
                             (Event.description == newEventData['eventDescription']) &
                             (Event.startDate == parser.parse(newEventData['eventStartDate'])))

    if 'eventId' not in newEventData and event.exists():
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


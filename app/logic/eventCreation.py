from dateutil import parser
from datetime import *

from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator

def validateNewEventData(newEventData):

    if parser.parse(newEventData['endDate'])  <  parser.parse(newEventData['startDate']):
        return (False, "Event start date is after event end date", newEventData)

    if parser.parse(newEventData['endDate']) ==   parser.parse(newEventData['startDate']) and newEventData['timeEnd'] <=  newEventData['timeStart']:
        return (False, "Event start time is after event end time", newEventData)

    if not newEventData['isRsvpRequired'] == 'on':
        if not isinstance(newEventData['isRsvpRequired'], bool):
            return (False, "Event RSVP must be a boolean", newEventData)

    if not newEventData['isTraining'] == 'on':
        if not isinstance(newEventData['isTraining'], bool):
            return (False, "Event Training must be a boolean", newEventData)


    if not newEventData['isService'] == 'on':
        if not isinstance(newEventData['isService'], bool):
            return (False, "Event Service Hours must be a boolean", newEventData)


    # Check for a pre-existing event with Event name, Description and Event Start date
    event = Event.select().where((Event.name == newEventData['name']) &
                             (Event.description == newEventData['description']) &
                             (Event.startDate == parser.parse(newEventData['startDate'])))

    if 'eventId' not in newEventData and event.exists():
        return (False, "This event already exists", newEventData)

    newEventData['valid'] = True
    return (True, "All inputs are valid.", newEventData)

def calculateRecurringEventFrequency(recurringEventInfo):
    """
    """

    name = recurringEventInfo['name']

    endDate = datetime.strptime(recurringEventInfo['endDate'], '%m-%d-%Y')
    startDate = datetime.strptime(recurringEventInfo['startDate'], '%m-%d-%Y')

    recurringEvents = []

    if endDate == startDate:
        raise Exception("This event is not a recurring Event")

    counter = 0
    for i in range(0, ((endDate-startDate).days +1), 7):
        counter += 1
        recurringEvents.append({'name': f"{name} Week {counter}",
                                'date':startDate.strftime('%m-%d-%Y'),
                                "week":counter})
        startDate += timedelta(days=7)

    return recurringEvents


def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['isRsvpRequired', 'isService', 'isTraining', 'isRecurring']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData

def preprocessEventData(incomingEventData):
    """
        Ensures that the event data dictionary is consistent before it reaches the template or event logic.

        - dates should be date objects
        - checkbaxes should be True or False
        - facilitators should be dictionaries (or objects?)
    """
    return {}

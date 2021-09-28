from dateutil import parser
import datetime

from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator

def validateNewEventData(newEventData):
    """
        Confirm that the provided data is valid for an event.

        Assumes the event data has been processed with `preprocessEventData`. NOT raw form data

        Returns 3 values: (boolean success, the validation error message, the data object)
    """

    if newEventData['isRecurring'] and newEventData['endDate']  <  newEventData['startDate']:
        return (False, "Event start date is after event end date", newEventData)

    if newEventData['endDate'] ==  newEventData['startDate'] and newEventData['timeEnd'] <=  newEventData['timeStart']:
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


    if 'eventId' not in newEventData:
        # Check for a pre-existing event with Event name, Description and Event Start date
        event = Event.select().where((Event.name == newEventData['name']) &
                                 (Event.description == newEventData['description']) &
                                 (Event.startDate == newEventData['startDate']))

        if event.exists():
            return (False, "This event already exists", newEventData)

    newEventData['valid'] = True
    return (True, "All inputs are valid.", newEventData)

def calculateRecurringEventFrequency(event):
    """
        Calculate the events to create based on a recurring event start and end date. Takes a 
        dictionary of event data.

        Assumes that the data has been processed with `preprocessEventData`. NOT raw form data.

        Return a list of events to create from the event data.
    """
    recurringEvents = []
    if event['endDate'] == event['startDate']:
        raise Exception("This event is not a recurring event")

    if not isinstance(event['endDate'], datetime.date) or not isinstance(event['startDate'], datetime.date):
        raise Exception("startDate and endDate must be datetime.date objects.")

    counter = 0
    for i in range(0, ((event['endDate']-event['startDate']).days +1), 7):
        counter += 1
        recurringEvents.append({'name': f"{event['name']} Week {counter}",
                                'date':event['startDate'],
                                "week":counter})
        event['startDate'] += datetime.timedelta(days=7)

    return recurringEvents

def preprocessEventData(eventData):
    """
        Ensures that the event data dictionary is consistent before it reaches the template or event logic.

        - dates should exist and be date objects if there is a value
        - checkbaxes should be True or False
        - facilitators should be a list of dictionaries (or objects?)
    """

    ## Process checkboxes
    eventCheckBoxes = ['isRsvpRequired', 'isService', 'isTraining', 'isRecurring']

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

    ## Process facilitators

    return eventData

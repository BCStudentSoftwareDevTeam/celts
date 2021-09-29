from dateutil import parser
import datetime

from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator

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

    if data['endDate'] ==  data['startDate'] and data['timeEnd'] <=  data['timeStart']:
        return (False, "Event start time is after event end time")

    if 'eventId' not in data:
        # Check for a pre-existing event with Event name, Description and Event Start date
        event = Event.select().where((Event.name == data['name']) &
                                 (Event.description == data['description']) &
                                 (Event.startDate == data['startDate']))

        if event.exists():
            return (False, "This event already exists")

    data['valid'] = True

    return (True, "All inputs are valid.")

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

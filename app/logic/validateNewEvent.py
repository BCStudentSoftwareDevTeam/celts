from app.models.event import Event
from datetime import *
from dateutil import parser
def validateNewEventData(newEventData, checkExists=True):

    if  newEventData['eventEndDate'] <  newEventData['eventStartDate']:
        return (False, "Event start date is after event end date", newEventData)


    if newEventData['eventEndDate'] ==  newEventData['eventStartDate'] and newEventData['eventEndTime'] <=  newEventData['eventStartTime']:
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
    event = Event.select().where((Event.eventName == newEventData['eventName']) &
                             (Event.description == newEventData['eventDescription']) &
                             (Event.startDate == parser.parse(newEventData['eventStartDate'])))

    if checkExists and event.exists():
        return (False, "This event already exists", newEventData)

    newEventData['valid'] = True
    return (True, "All inputs are valid.", newEventData)

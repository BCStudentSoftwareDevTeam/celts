from app.models.event import Event

def validateNewEventData(newEventData):

    if  newEventData['eventEndDate'] <  newEventData['eventStartDate']:
        return (False, "Event start date is after event end date")


    if newEventData['eventEndDate'] ==  newEventData['eventStartDate'] and newEventData['eventEndTime'] <=  newEventData['eventStartTime']:
        return (False, "Event start time is after event end time")


    if newEventData['eventIsTraining'] == 'on' and newEventData['eventRequiredForProgram'] == False: #default value for checked button is on
        return (False, "A training event must be required for the program.")


    # Event name, Description and Event Start date
    event = Event.select().where((Event.eventName == newEventData['eventName']) &
                             (Event.description == newEventData['eventDescription']) &
                             (Event.startDate == newEventData['eventStartDate']))
    # if event.exists():
    #     return (False, "This event already exists")

    return (True, "All inputs are valid.")

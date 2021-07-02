from app.models.event import Event

def validateNewEventData(newEventData):

    if  newEventData['eventEndDate'] <  newEventData['eventStartDate']:
        return (False, "Event start date is after event end date")


    if newEventData['eventEndTime'] <=  newEventData['eventStartTime']:
        return (False, "Event start time is after event end time")

    # Event name, Description and Event Start date
    event = Event.select().where((Event.eventName == newEventData['eventName']) &
                             (Event.description == newEventData['eventDescription']) &
                             (Event.startDate == newEventData['eventStartDate']))
    if event.exists():
        return (False, "This event already exists")

    return (True, "All inputs are valid.")

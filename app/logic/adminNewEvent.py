from app.models.event import Event
from app.models.facilitator import Facilitator

def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData

def createNewEvent(newEventData):

    eventEntry = Event.create(eventName = newEventData['eventName'],
                              term = newEventData['eventTerm'],
                              description= newEventData['eventDescription'],
                              timeStart = newEventData['eventStartTime'],
                              timeEnd = newEventData['eventEndTime'],
                              location = newEventData['eventLocation'],
                              isRecurring = newEventData['recurringEvent'],
                              isRsvpRequired = newEventData['eventRSVP'],
                              isRequiredForProgram = newEventData['eventRequiredForProgram'],
                              isTraining = newEventData['eventIsTraining'],
                              isService = newEventData['eventServiceHours'],
                              startDate =  newEventData['eventStartDate'],
                              endDate =  newEventData['eventEndDate'],
                              program = newEventData['programId'])

    facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                          event = eventEntry )

def eventEdit(newEventData):

    term = Term.select(Term.id).where(Term.description == newEventData['eventTerm'])
    eventId = newEventData['eventId']
    eventInfo = Event.get_by_id(eventId)
    print(newEventData['programId'])
    eventData = {
            "id": eventId,
            "program": newEventData['programId'],
            "term": term,
            "eventName": newEventData['eventName'],
            "description": newEventData['eventDescription'],
            "timeStart": newEventData['eventStartTime'],
            "timeEnd": newEventData['eventEndTime'],
            "location": newEventData['eventLocation'],
            "startDate": newEventData['eventStartDate'],
            "endDate": newEventData['eventEndDate']
        }
    eventEntry = Event.insert_many(eventData).on_conflict_replace().execute()

    facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                          event = eventEntry )

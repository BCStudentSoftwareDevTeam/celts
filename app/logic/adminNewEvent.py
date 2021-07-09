
from app.models.term import Term
from app.models.event import Event
from app.models.facilitator import Facilitator

def manageNewEventData(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData

def createEvent(newEventData):

    term = Term.select(Term.id).where(Term.description == newEventData['eventTerm'])
    print(term)

    eventEntry = Event.create(eventName = newEventData['eventName'],
                              term_id = term,
                              description= newEventData['eventDescription'],
                              timeStart = newEventData['eventStartTime'],
                              timeEnd = newEventData['eventEndTime'],
                              location = newEventData['eventLocation'],
                              isRecurring = newEventData['recurringEvent'],
                              isRsvpRequired = newEventData['eventRSVP'], #rsvp
                              isRequiredForProgram = newEventData['eventRequiredForProgram'],
                              isTraining = newEventData['eventIsTraining'],
                              isService = newEventData['eventServiceHours'],
                              startDate =  newEventData['eventStartDate'],
                              endDate =  newEventData['eventEndDate'],
                              program_id = newEventData['programId'])

    eventID = Event.select(Event.id).where((Event.eventName == newEventData['eventName']) &
                                           (Event.description == newEventData['eventDescription']) &
                                           (Event.startDate == newEventData['eventStartDate']))

    facilitatorEntry = Facilitator.create(user_id = newEventData['eventFacilitator'],
                                          event_id = eventID )

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


    eventID = Event.select(Event.id).where((Event.eventName == newEventData['eventName']) &
                                           (Event.description == newEventData['eventDescription']) &
                                           (Event.startDate == newEventData['eventStartDate']))

    facilitatorEntry = Facilitator.get_or_create(user_id = newEventData['eventFacilitator'],
                                                event_id = eventId )

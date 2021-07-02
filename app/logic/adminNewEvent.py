
from app.models.term import Term
from app.models.event import Event
from app.models.facilitator import Facilitator

def manageNewEventData(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours' ]

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = 0

    return(eventData)

def createEvent(newEventData):

    term = Term.select(Term.id).where(Term.description == newEventData['eventTerm'])

    eventEntry = Event.create(eventName = newEventData['eventName'],
                              term_id = term,
                              description= newEventData['eventDescription'],
                              timeStart = newEventData['eventStartTime'],
                              timeEnd = newEventData['eventEndTime'],
                              location = newEventData['eventLocation'],
                              isRecurring = newEventData['recurringEvent'],
                              isRsvpRequired = newEventData['eventRSVP'], #rsvp
                              isRequiredForProgram = newEventData['eventRequiredForProgram'],
                              isService= newEventData['eventServiceHours'],
                              startDate =   newEventData['eventStartDate'],
                              endDate =  newEventData['eventEndDate'],
                              program_id = newEventData['programId'])

    eventID = Event.select(Event.id).where((Event.eventName == newEventData['eventName']) &
                                           (Event.description == newEventData['eventDescription']) &
                                           (Event.startDate == newEventData['eventStartDate']))

    facilitatorEntry = Facilitator.create(user_id = newEventData['eventFacilitator'],
                                          event_id = eventID )

from app.models.event import Event
from datetime import *
from app.models.facilitator import Facilitator


def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining', 'eventIsRecurring']

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
                              isRecurring = newEventData['eventIsRecurring'],
                              isRsvpRequired = newEventData['eventRSVP'],
                              isPrerequisiteForProgram = newEventData['eventRequiredForProgram'],
                              isTraining = newEventData['eventIsTraining'],
                              isService = newEventData['eventServiceHours'],
                              startDate =  newEventData['eventStartDate'],
                              endDate =  newEventData['eventEndDate'],
                              program = newEventData['programId'])

    facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                              event = eventEntry)

    return (eventEntry)

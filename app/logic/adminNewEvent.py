from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models import mainDB
from datetime import *
from app.models.facilitator import Facilitator


def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining', 'eventIsRecurring']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData

def createNewEvent(newEventData):
    """
    Creates a new event and facilitator for that event
    The newEventData must have gone through the validateNewEventData function
    for 'valid' to be True.

    param: newEventData - dict with the event information
    """


    if newEventData['valid'] == True:
        # get the program first so if there's an exception we don't create the other stuff
        program = Program.get_by_id(newEventData['programId'])

        with mainDB.atomic():
            newEvent = Event.create(eventName = newEventData['eventName'],
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
                                  endDate =  newEventData['eventEndDate'])


            programEvent = ProgramEvent.create(program=program, event=newEvent)

            facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                                      event = newEvent)
        return newEvent
    else:
        raise Exception("Invalid Data")

def eventEdit(newEventData):

    if newEventData['valid'] == True:

        eventId = newEventData['eventId']
        eventData = {
                "id": eventId,
                "term": newEventData['eventTerm'],
                "eventName": newEventData['eventName'],
                "description": newEventData['eventDescription'],
                "timeStart": newEventData['eventStartTime'],
                "timeEnd": newEventData['eventEndTime'],
                "location": newEventData['eventLocation'],
                "isRecurring": newEventData['eventIsRecurring'],
                "isTraining": newEventData['eventIsTraining'],
                "isRsvpRequired": newEventData['eventRSVP'],
                "isService": newEventData['eventServiceHours'],
                "startDate": newEventData['eventStartDate'],
                "endDate": newEventData['eventEndDate']

            }
        eventEntry = Event.update(**eventData).where(Event.id == eventId).execute()

        if Facilitator.get_or_none(Facilitator.event == eventId):
            updateFacilitator = (Facilitator.update(user = newEventData['eventFacilitator'])
                                            .where(Facilitator.event == eventId)).execute()

        else:
            facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                                      event = eventId)


    else:
        raise Exception("Invalid Data")

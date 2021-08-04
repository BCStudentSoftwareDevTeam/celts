from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models import mainDB
from datetime import *
from app.models.facilitator import Facilitator
from app.controllers.admin import admin_bp
from flask import request
from dateutil import parser

def calculateRecurringEventFrequency(recurringEventInfo):
    """
    """

    eventName = recurringEventInfo['eventName']

    endDate = datetime.strptime(recurringEventInfo['eventEndDate'], '%m-%d-%Y')
    startDate = datetime.strptime(recurringEventInfo['eventStartDate'], '%m-%d-%Y')

    recurringEvents = []

    if endDate == startDate:
        raise Exception("This event is not a recurring Event")

    counter = 0
    for i in range(0, ((endDate-startDate).days +1), 7):
        counter += 1
        recurringEvents.append({'eventName': f"{eventName} Week {counter}",
                                'date':startDate.strftime('%m-%d-%Y'),
                                "week":counter})
        startDate += timedelta(days=7)

    return recurringEvents


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

        eventsToCreate = []
        if newEventData['eventIsRecurring'] == 'on':
            eventsToCreate = calculateRecurringEventFrequency(newEventData)
        else:
            eventsToCreate.append({'eventName': f"{newEventData['eventName']}",
                                    'date':newEventData['eventStartDate'],
                                    "week":1})

        for eventInstance in eventsToCreate:
            with mainDB.atomic():
                newEvent = Event.create(eventName = eventInstance['eventName'],
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
                                          startDate =  parser.parse(eventInstance['date']),
                                          endDate =  parser.parse(eventInstance['date']))

                programEvent = ProgramEvent.create(program=program, event=newEvent)

                facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],event = newEvent)

    else:
        raise Exception("Invalid Data")

    return newEvent

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
                "startDate": parser.parse(newEventData['eventStartDate']),
                "endDate": parser.parse(newEventData['eventEndDate'])

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

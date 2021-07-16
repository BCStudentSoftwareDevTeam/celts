from app.models.event import Event
from datetime import *
from app.models.facilitator import Facilitator
from app.controllers.admin import admin_bp
from flask import request
import json


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
                                'Date':startDate.strftime('%m-%d-%Y'),
                                "week":counter})
        startDate += timedelta(days=7)

    return json.dumps(recurringEvents)


def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining', 'eventIsRecurring']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData

def createNewEvent(newEventData):

    try:
        if newEventData['eventIsRecurring'] == 'on':
            for entry in range(1,len(newEventData)):
                if f"week{entry}" in newEventData:
                    eventEntry = Event.create(eventName = (newEventData['eventName']+f" Week {entry}"),
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
                                              startDate =  newEventData[f"week{entry}"],
                                              endDate =  newEventData[f"week{entry}"],
                                              program = newEventData['programId'])

                    facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                                              event = eventEntry)
                else:
                    break

            return ("Recurring Events successfully created!")
        else:
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

            return ("Event successfully created!")

    except:
        raise

from app.models.event import Event
from app.models.facilitator import Facilitator
import datetime

def setValueForUncheckedBox(eventData):

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours', 'eventIsTraining']

    for checkBox in eventCheckBoxes:
        if checkBox not in eventData:
            eventData[checkBox] = False

    return eventData
#
# def setDateFormatYMD(eventData):
#
#     newEventData['eventStartDate'] = datetime.datetime.strptime(newEventData['eventStartDate'], '%m-%d-%Y').strftime('%Y-%m-%d')
#     newEventData['eventEndDate'] = datetime.datetime.strptime(newEventData['eventEndDate'], '%m-%d-%Y').strftime('%Y-%m-%d')
#     newEventData['eventStartDate'] = setDateFormatYMD(newEventData['eventStartDate'])
#
#     eventStartDate = datetime.datetime.strptime(newEventData['eventStartDate'], '%m-%d-%Y').strftime('%Y-%m-%d')
#     eventEndDate = datetime.datetime.strptime(newEventData['eventEndDate'], '%m-%d-%Y').strftime('%Y-%m-%d')


def createNewEvent(newEventData):


    eventEntry = Event.create(eventName = newEventData['eventName'],
                              term = newEventData['eventTerm'],
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
                              program = newEventData['programId'])

    facilitatorEntry = Facilitator.create(user = newEventData['eventFacilitator'],
                                          event = eventEntry )

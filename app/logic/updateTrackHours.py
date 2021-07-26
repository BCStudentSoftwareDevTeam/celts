# from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from datetime import datetime
from app.models.user import User


def getEventLengthInHours(startTime, endTime, eventDate):
    """
    Converts the event length hours into decimal
    parameters: startTime- start time event (type: time)
                endTime- end time event (type: time)
                eventDate- date of the event (type: datetime)
    """
    #can only subtract datetime objects, not time objects. So convert time into datetime
    eventLength = datetime.combine(eventDate, endTime) - datetime.combine(eventDate, startTime)
    eventLengthInHours = round(eventLength.seconds/3600, 2)
    return eventLengthInHours


def updateTrackHours(participantData):
    """
    updates the events participant table with data from the track hours webpage

    param: participantData- a dictionary that contains data from every row of the page along with the associated username.
    """

    for user in range(1, len(participantData)):
        if f'username{user}' in participantData:
            username = participantData[f'username{user}']
            if (User.get_or_none(User.username == username)):

                try:
                    if participantData['checkbox_'+ username] == "on": #if the user is marked as present
                        (EventParticipant.update({EventParticipant.hoursEarned: float(participantData['inputHours_'+ username]),EventParticipant.attended: True}).where(EventParticipant.event == participantData['event'],
                                                 EventParticipant.user == participantData[f'username{user}'])).execute()

                except:   #if there is no checkbox for user then they are not present for the event.
                    (EventParticipant.update({EventParticipant.attended: False, EventParticipant.hoursEarned: 0}).where(EventParticipant.event == participantData['event'],
                        EventParticipant.user == participantData[f'username{user}'])).execute()
            else:
                raise Exception("Volunteer does not exist")
        else:
            break

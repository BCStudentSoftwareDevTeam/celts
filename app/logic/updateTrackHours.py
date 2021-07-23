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
                        (EventParticipant.update({EventParticipant.hoursEarned: float(participantData['inputHours_'+ username])}).where(EventParticipant.event == participantData['event'],
                                                 EventParticipant.user == participantData[f'username{user}'])).execute()

                        (EventParticipant.update({EventParticipant.attended: True}).where(EventParticipant.event == participantData['event'],
                                                 EventParticipant.user == participantData[f'username{user}'])).execute()
                except:   #if there is no checkbox for user then they are not present for the event.
                    (EventParticipant.update({EventParticipant.attended: False}).where(EventParticipant.event == participantData['event'],
                        EventParticipant.user == participantData[f'username{user}'])).execute()

                    (EventParticipant.update({EventParticipant.hoursEarned: 0}).where(EventParticipant.event == participantData['event'],
                                             EventParticipant.user == participantData[f'username{user}'])).execute()
            else:
                return "Volunteer does not exist."
        else:
            break

    return "Volunteer table successfully updated!"



def addVolunteerToEvent(user, volunteerEventID, eventLengthInHours):
    '''
    Adds a volunteer to the eventparticipant table database after a search and click to 'Add participant' button
    param: user- string containing first name, last name, and username (format: "<firstName> <lastName> (<username>)")
           volunteerEventID - id of the event the volunteer is being registered for
           eventLengthInHours - how long the event lasts (how may hours to give the student) (type: float)
    '''
    try:
        user = user.strip("()")
        userName=user.split('(')[-1]

        alreadyVolunteered = (EventParticipant.select().where(EventParticipant.user==userName, EventParticipant.event==volunteerEventID)).exists()
        if alreadyVolunteered:
            return("Volunteer already exists.")
        else:
            EventParticipant.create(user=userName, event = volunteerEventID, attended = True, hoursEarned = eventLengthInHours)
            return "Volunteer successfully added!"

    except Exception as e:
        return "Error when adding volunteer", 500

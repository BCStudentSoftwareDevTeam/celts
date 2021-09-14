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


def updateVolunteers(participantData):
    """
    updates the events participant table with data from the track Volunteer webpage

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

                except (KeyError):   #if there is no checkbox for user then they are not present for the event.
                    (EventParticipant.update({EventParticipant.attended: False, EventParticipant.hoursEarned: 0}).where(EventParticipant.event == participantData['event'],
                        EventParticipant.user == participantData[f'username{user}'])).execute()
                except Exception as e:
                    print(e)
                    return False
            else:
                return False
        else:
            break
    return True


def addVolunteerToEvent(user, volunteerEventID, eventLengthInHours):
    '''
    Adds a volunteer to eventparticipant table if they don't already exist in that table.
    Adds a volunteer to the eventparticipant table database after a search and click to 'Add participant' button
    param: user- string containing username)
           volunteerEventID - id of the event the volunteer is being registered for
           eventLengthInHours - how long the event lasts (how may hours to give the student) (type: float)
    '''
    try:
        if not EventParticipant.get_or_none(user=user, event = volunteerEventID):
            EventParticipant.create(user=user, event = volunteerEventID, attended = True, hoursEarned = eventLengthInHours, rsvp = True)
        return True

    except Exception as e:
        return False

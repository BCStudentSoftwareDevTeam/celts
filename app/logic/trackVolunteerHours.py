# present/ RSVped/Total Hours (eventparticipant: also has username)
# Role (Pending)
# Email/Phone Number/name (user table)
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from datetime import datetime

def eventLengthInHours(startTime, endTime, eventDate):

    #can only subtract datetime objects, not time objects. So convert time into datetime
    eventLength = datetime.combine(eventDate, endTime) - datetime.combine(eventDate, startTime)
    (h, m, s) = str(eventLength).split(':')
    decimalEventLength = int(h) + round(int(m) / 60, 2)

    return decimalEventLength

def trackVolunteerHours():
    """
    This function gets the data from the database so that we could use them in the UI.
    """
    trackHours = EventParticipant.select()

    return trackHours

# present/ RSVped/Total Hours (eventparticipant: also has username)
# Role (Pending)
# Email/Phone Number/name (user table)
from app.models.eventParticipant import EventParticipant
from app.models.user import User

def trackVolunteerHours():
    """
    This function gets the data from the database so that we could use them in the UI.
    """
    trackHours = EventParticipant.select()

    return trackHours

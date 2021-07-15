from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from peewee import fn

def trackVolunteerHours():
    """
    This function gets the data from the database so that we could use them in the UI.
    """
    trackHours = EventParticipant.select()

    return trackHours

def prereqParticipants(programID, prlist):
    """
    This function tracks the users who have attended every Prerequisite
    event and adds them to a list that will not flag them when tracking hours.
    """
    eventPreqDataList = [participant.user.username for participant in (EventParticipant.select().where(EventParticipant.event.in_(prlist)))]
    attendedPreq = list(dict.fromkeys(filter(lambda user: eventPreqDataList.count(user) == len(prlist), eventPreqDataList)))
    return attendedPreq

from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from peewee import fn

def trainedParticipants(programID, trlist):
    """
    This function tracks the users who have attended every Prerequisite
    event and adds them to a list that will not flag them when tracking hours.
    """
    eventTrainingDataList = [participant.user.username for participant in (EventParticipant.select().where(EventParticipant.event.in_(trlist)))]
    attendedTraining = list(dict.fromkeys(filter(lambda user: eventTrainingDataList.count(user) == len(trlist), eventTrainingDataList)))
    return attendedTraining

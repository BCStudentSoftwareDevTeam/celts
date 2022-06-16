from app.models.eventParticipant import EventParticipant
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.backgroundCheck import BackgroundCheck
from app.models.studentManager import StudentManager
from datetime import datetime, date
from app.logic.adminLogs import createLog
from app.logic.events import getEvents





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


def updateEventParticipants(participantData):
    """
    Create new entry in event participant table if user does not exist. Otherwise, updates the record.

    param: participantData- a dictionary that contains data from every row of the page along with the associated username.
    """
    event = Event.get_or_none(Event.id==participantData['event'])
    if not event:
        raise Exception("Event does not exist.") # ???
        return False

    for user in range(1, len(participantData)):
        if f'username{user}' in participantData:
            username = participantData[f'username{user}']
            userObject = User.get_or_none(User.username==username)
            eventParticipant = EventParticipant.get_or_none(user=userObject, event=participantData['event'])
            if userObject:
                try:
                    if participantData[f'checkbox_{username}']: #if the user is marked as present
                        hoursEarned = float(participantData['inputHours_'+ username])
                        if eventParticipant:
                            ((EventParticipant
                                .update({EventParticipant.hoursEarned: hoursEarned})
                                .where(
                                    EventParticipant.event==event.id,
                                    EventParticipant.user==userObject.username))
                                .execute())
                        else:
                            (EventParticipant
                                .create(
                                    user=userObject,
                                    event=event,
                                    hoursEarned=hoursEarned))
                except (KeyError):
                    if eventParticipant:
                        ((EventParticipant.delete()
                            .where(
                                EventParticipant.user==userObject.username,
                                EventParticipant.event==event.id))
                            .execute())
            else:
                return False
        else:
            break
    return True


def addVolunteerToEventRsvp(user, volunteerEventID):
    '''
    Adds a volunteer to event rsvp table when a user rsvps and when they are
    added through the track volunteer page by an admin.

    param: user - a string containing username
           volunteerEventID - id of the event the volunteer is being registered for
    '''
    try:
        if not EventRsvp.get_or_none(user=user, event=volunteerEventID):
            EventRsvp.create(user=user, event=volunteerEventID)
        return True

    except Exception as e:
        return False

def setUserBackgroundCheck(user,bgType, checkPassed):
    today = date.today()
    user = User.get_by_id(user)
    deleteInstance = BackgroundCheck.delete().where(BackgroundCheck.user == user, BackgroundCheck.type == bgType)
    deleteInstance.execute()
    update = BackgroundCheck.create(user=user, type=bgType, passBackgroundCheck=checkPassed, datePassed=today)
    update.save()
    createLog(f"Updated {user.firstName} {user.lastName}'s background check for {bgType} to {bool(checkPassed)}.")

def getProgramManagerForEvent(studentManager, event= None, programId = None):
    """
    This function checks to see if a user is a student manager for an event.
    NOTE: this function needs either the event or programId parameters to work
    studentManager: expects a user peewee object
    event: expects an event peewee object
    programId: expects an int that is the primary ID of a program in the database.
    """
    if event:
        programId = ProgramEvent.select().where(ProgramEvent.event == event)

    programManagerResult = StudentManager.select().where(StudentManager.user == studentManager,
                                                        StudentManager.program == programId[0].program)
    return programManagerResult

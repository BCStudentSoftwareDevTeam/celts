from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from app.models.eventRsvp import EventRsvp
from app.models.program import Program
from app.models.backgroundCheck import BackgroundCheck
from app.models.programManager import ProgramManager
from datetime import datetime, date
from app.logic.createLogs import createActivityLog
from app.models.eventLabor import EventLabor

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


def updateEventLabor(participantData):
    """
    Create new entry in event labor table if user does not exist. Otherwise, updates the record.

    param: participantData- an ImmutableMultiDict that contains data from every row of the page along with the associated username.
    """
    event = Event.get_or_none(Event.id==participantData['event'])
    if not event:
        raise Exception("Event does not exist.") # ???
        return False


    for username in participantData.getlist("username"):
        userObject = User.get_or_none(User.username==username)
        eventLabor = EventLabor.get_or_none(user=userObject, event=participantData['event'])
        if userObject:
            if participantData.get(f'checkbox_{username}'): #if the user is marked as present
                inputHours = participantData.get(f'inputHours_{username}')
                hoursWorked = float(inputHours) if inputHours else 0
                if eventLabor:
                    ((EventLabor.update({EventLabor.hoursWorked: hoursWorked})
                                      .where(EventLabor.event==event.id, EventLabor.user==userObject.username))
                                      .execute())
                else:
                    EventLabor.create(user=userObject, event=event, hoursWorked=hoursWorked)
            else:
                ((EventLabor.delete()
                                  .where(EventLabor.user==userObject.username, EventLabor.event==event.id))
                                  .execute())
        else:
            return False
    return True

def addUserBackgroundCheck(user, bgType, bgStatus, dateCompleted):
    """
    Changes the status of a users background check depending on what was marked
    on their volunteer profile.
    """
    today = date.today()
    user = User.get_by_id(user)
    if bgStatus == '' and dateCompleted == '':
        createActivityLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as 'in progress'.")
    else:
        if not dateCompleted:
            dateCompleted = None
        update = BackgroundCheck.create(user=user, type=bgType, backgroundCheckStatus=bgStatus, dateCompleted=dateCompleted)
        if bgStatus == 'Submitted':
            createActivityLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as submitted.")
        elif bgStatus == 'Passed':
            createActivityLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as passed.")
        else:
            createActivityLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as failed.")

def deleteUserBackgroundCheck(bgCheckId, user):
    """
    Deletes the user's background check by marking it as deleted with a timestamp and user information.
    """
    bgCheck = BackgroundCheck.get_or_none(BackgroundCheck.id == bgCheckId)

    if bgCheck:
        (BackgroundCheck.update({BackgroundCheck.deletionDate: datetime.now(), BackgroundCheck.deletedBy: user})
                         .where(BackgroundCheck.id == bgCheck.id)
                         .execute())

def setProgramManager(username, program_id, action):
    '''
    Assigns or removes a user as a student manager for a program.

    param: username - a string
           program_id - id
           action: add, remove

    '''
    programManager = User.get(User.username==username)
    if action == "add":
        programManager.addProgramManager(program_id)
    elif action == "remove":
        programManager.removeProgramManager(program_id)


def getLaborStudents(event):
    eventLabor = (EventLabor.select(EventLabor, User)
                                         .join(User)
                                         .where(EventLabor.event == event))

    return [p for p in eventLabor]



def sortLabor(event):

    eventLabor = getLaborStudents(event)

    eventLaborData = eventLabor

    return eventLaborData, eventLabor

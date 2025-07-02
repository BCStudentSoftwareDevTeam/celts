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
    event = Event.get_or_none(Event.id == participantData['event'])
    if not event:
        return False

    for username in participantData.getlist("username"):
        userObject = User.get_or_none(User.username == username)
        if not userObject:
            continue

        eventLabor = EventLabor.get_or_none(user=userObject, event=event)
        checkbox_value = participantData.get(f'checkbox_{username}', 'off')
        didWork = checkbox_value == "on"

        if eventLabor:
            (EventLabor.update({
                EventLabor.didWork: didWork
            })
            .where(EventLabor.event == event.id, EventLabor.user == userObject.username)
            .execute())
        else:
            EventLabor.create(
                user=userObject,
                event=event,
                didWork=didWork
            )

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

def checkUserLabor(user,  event):
    return EventLabor.select().where(EventLabor.user == user, EventLabor.event == event).exists()


def addStudentLaborToEvent(user, event):
    """
        Add a user to an event.
        If the event is in the past, add the user as a volunteer (EventParticipant)
        If the event is in the future, rsvp for the user (EventRsvp)

        Returns True if the operation was successful, false otherwise
    """
    try:
        LaborExists = checkUserLabor(user, event)
        if not LaborExists:
            EventLabor.create(user=user, event=event, didWork=False)
        if LaborExists:
            return "already in"
    except Exception as e:
        print(e)
        return False

    return True

def unattendedRequiredEvents(program, user):
    requiredEvents = (Event.select(Event)
                           .where(Event.isTraining == True, Event.program == program))

    if requiredEvents:
        attendedRequiredEventsList = []
        for event in requiredEvents:
            attendedRequirement = (EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event == event))
            if not attendedRequirement:
                attendedRequiredEventsList.append(event.name)
        if attendedRequiredEventsList is not None:
            return attendedRequiredEventsList
    else:
        return []
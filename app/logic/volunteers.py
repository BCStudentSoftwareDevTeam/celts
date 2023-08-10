from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from app.models.program import Program
from app.models.backgroundCheck import BackgroundCheck
from app.models.programManager import ProgramManager
from datetime import datetime, date
from app.logic.createLogs import createAdminLog

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

    param: participantData- an ImmutableMultiDict that contains data from every row of the page along with the associated username.
    """
    event = Event.get_or_none(Event.id==participantData['event'])
    if not event:
        raise Exception("Event does not exist.") # ???
        return False


    for username in participantData.getlist("username"):
        userObject = User.get_or_none(User.username==username)
        eventParticipant = EventParticipant.get_or_none(user=userObject, event=participantData['event'])
        if userObject:
            if participantData.get(f'checkbox_{username}'): #if the user is marked as present
                inputHours = participantData.get(f'inputHours_{username}')
                hoursEarned = float(inputHours) if inputHours else 0
                if eventParticipant:
                    ((EventParticipant.update({EventParticipant.hoursEarned: hoursEarned})
                                      .where(EventParticipant.event==event.id, EventParticipant.user==userObject.username))
                                      .execute())
                else:
                    EventParticipant.create(user=userObject, event=event, hoursEarned=hoursEarned)
            else:
                ((EventParticipant.delete()
                                  .where(EventParticipant.user==userObject.username, EventParticipant.event==event.id))
                                  .execute())
        else:
            return False
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

def addUserBackgroundCheck(user, bgType, bgStatus, dateCompleted):
    """
    Changes the status of a users background check depending on what was marked
    on their volunteer profile.
    """
    today = date.today()
    user = User.get_by_id(user)
    if bgStatus == '' and dateCompleted == '':
        createAdminLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as 'in progress'.")
    else:
        if not dateCompleted:
            dateCompleted = None
        update = BackgroundCheck.create(user=user, type=bgType, backgroundCheckStatus=bgStatus, dateCompleted=dateCompleted)
        if bgStatus == 'Submitted':
            createAdminLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as submitted.")
        elif bgStatus == 'Passed':
            createAdminLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as passed.")
        else:
            createAdminLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as failed.")

def setProgramManager(username, program_id, action):
    '''
    adds and removes the studentstaff from program that makes them student manager.

    param: uername - a string
           program_id - id
           action: add, remove

    '''
    studentstaff=User.get(User.username==username)
    if action == "add" and studentstaff.isCeltsStudentStaff==True:
        studentstaff.addProgramManager(program_id)
    elif action == "remove":
        studentstaff.removeProgramManager(program_id)

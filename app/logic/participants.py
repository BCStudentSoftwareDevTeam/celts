from flask import g
from peewee import fn, JOIN
from datetime import date
from app.models.user import User
from app.models.event import Event
from app.models.term import Term
from app.models.eventRsvp import EventRsvp
from app.models.program import Program
from app.models.eventParticipant import EventParticipant
from app.logic.users import isEligibleForProgram
from app.logic.sharedLogic import getEventLengthInHours
from app.logic.events import getEventRsvpCountsForTerm
from app.logic.createLogs import createRsvpLog
from collections import defaultdict
from app.models.backgroundCheck import BackgroundCheck
from app.models.programManager import ProgramManager
from datetime import datetime, date
from app.logic.createLogs import createActivityLog

# ---------------------- Volunteer Stuff ----------------------

def trainedParticipants(programID, targetTerm):
    """
    This function tracks the users who have attended every Prerequisite
    event and adds them to a list that will not flag them when tracking hours.
    Returns a list of user objects who've completed all training events.
    """

    # Reset program eligibility each term for all other trainings
    isRelevantAllVolunteer = (Event.isAllVolunteerTraining) & (Event.term.academicYear == targetTerm.academicYear) 
    isRelevantProgramTraining = (Event.program == programID) & (Event.term == targetTerm) & (Event.isTraining) 
    allTrainings = (Event.select()
                         .join(Term)
                         .where(isRelevantAllVolunteer | isRelevantProgramTraining, 
                                Event.isCanceled == False))

    fullyTrainedUsers = (User.select()
                             .join(EventParticipant)
                             .where(EventParticipant.event.in_(allTrainings))
                             .group_by(EventParticipant.user)
                             .having(fn.Count(EventParticipant.user) == len(allTrainings)).order_by(User.username))

    return list(fullyTrainedUsers)

def checkUserRsvp(user,  event):
    return EventRsvp.select().where(EventRsvp.user==user, EventRsvp.event == event).exists()
    
def getEventParticipants(event, laborCheck): 
    if laborCheck  == True:
        eventVolunteers = (EventParticipant.select(EventParticipant, User)
                                         .join(User)
                                         .where((EventParticipant.event == event) & (EventParticipant.isLabor == True)))
    else:
        eventVolunteers = (EventParticipant.select(EventParticipant, User)
                                            .join(User)
                                            .where((EventParticipant.event == event) & (EventParticipant.isLabor == False)))

    return [p for p in eventVolunteers]

def unattendedRequiredEvents(program, user):

    # Check for events that are prerequisite for program
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


def getParticipationStatusForTrainings(program, userList, term):
    """
    This function returns a dictionary of all trainings for a program and
    whether the current user participated in them.

    :returns: trainings for program and if the user participated
    """
    isRelevantTraining = ((Event.isAllVolunteerTraining | ((Event.isTraining) & (Event.program == program))) & 
                              (Event.term.academicYear == term.academicYear))
    programTrainings = (Event.select(Event, Term, EventParticipant, EventRsvp)
                             .join(EventParticipant, JOIN.LEFT_OUTER).switch()
                             .join(EventRsvp, JOIN.LEFT_OUTER).switch()
                             .join(Term)
                             .where(isRelevantTraining, (Event.isCanceled != True)).order_by(Event.startDate))

    # Create a dictionary where the keys are trainings and values are a set of those who attended
    trainingData = defaultdict(set)
    for training in programTrainings:
        try:
            if training.isPastStart:
                trainingData[training].add(training.eventparticipant.user_id)
            else:  # The training has yet to happen
                trainingData[training].add(training.eventrsvp.user_id)
        except AttributeError:
            pass
    # Create a dictionary binding usernames to a list of [training, hasAttended] pairs. The tuples consist of the training (event object) and whether or not they attended it (bool)

    # Necessarily complex algorithm to merge the attendances of trainings which have the same name
    # Structure of userParticipationStatus for a single user:
    # {user.username: {training1.name: [EventObject, hasAttended], training2.name: [EventObject, hasAttended]}, ...}
    userParticipationStatus = {user.username: {} for user in userList}
    for training, attendeeList in trainingData.items():
        for user in userList:
            if training.name not in userParticipationStatus[user.username] or user.username in attendeeList:
                userParticipationStatus[user.username][training.name] = [training, user.username in attendeeList]
    
    return {user.username: list(userParticipationStatus[user.username].values()) for user in userList}


def sortParticipantsByStatus(event):
    """
    Takes in an event object, queries all participants, and then filters those
    participants by their attendee status.

    return: a list of participants who didn't attend, a list of participants who are waitlisted,
    a list of participants who attended, and a list of all participants who have some status for the 
    event.
    """
    eventVolunteers = getEventParticipants(event, False)

    # get all RSVPs for event and filter out those that did not attend into separate list
    eventRsvpData = list(EventRsvp.select(EventRsvp, User).join(User).where(EventRsvp.event==event).order_by(EventRsvp.rsvpTime))
    eventNonAttendedData = [rsvp for rsvp in eventRsvpData if rsvp.user not in eventVolunteers]

    if event.isPastStart:
        eventVolunteerData = eventVolunteers

        # if the event date has passed disregard the waitlist
        eventWaitlistData = []
    else:
        # if rsvp is required for the event, grab all volunteers that are in the waitlist
        eventWaitlistData = [volunteer for volunteer in (eventVolunteers + eventRsvpData) if volunteer.rsvpWaitlist and event.isRsvpRequired]
        
        # put the rest of the users that are not on the waitlist into the volunteer data
        eventVolunteerData = [volunteer for volunteer in eventNonAttendedData if volunteer not in eventWaitlistData]
        eventNonAttendedData = []
    
    return eventNonAttendedData, eventWaitlistData, eventVolunteerData, eventVolunteers


def updateEventVolunteers(participantData):
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

def addUserBackgroundCheck(user, bgType, bgStatus, dateCompleted):
    """
    Changes the status of a users background check depending on what was marked
    on their volunteer profile.
    """
    today = date.today()
    user = User.get_by_id(user)
    if bgStatus == '' and dateCompleted == '':
        createActivityLog(f"Marked {user.firstName} {user.lastName}'s background check for {bgType} as 'Draft'.")
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

def addVolunteerToEvent(user, event):
    """
        Add a user to an event.
        If the event is in the past, add the user as a volunteer (EventParticipant) including hours worked.
        If the event is in the future, rsvp for the user (EventRsvp)

        Returns True if the operation was successful, false otherwise
    """
    try:
        volunteerExists = checkUserParticipant(user, event, False)
        rsvpExists = checkUserRsvp(user, event)
        if event.isPastStart:
            if not volunteerExists:
                # We duplicate these two lines in addBnumberAsParticipant
                eventHours = getEventLengthInHours(event.timeStart, event.timeEnd, event.startDate)
                EventParticipant.create(user = user, event = event, hoursEarned = eventHours)
        else:
            if not rsvpExists:
                currentRsvp = getEventRsvpCountsForTerm(event.term)
                waitlist = currentRsvp[event.id] >= event.rsvpLimit if event.rsvpLimit is not None else 0
                EventRsvp.create(user = user, event = event, rsvpWaitlist = waitlist)

                targetList = "the waitlist" if waitlist else "the RSVP list"
                if g.current_user.username == user.username:
                    createRsvpLog(event.id, f"{user.fullName} joined {targetList}.")
                else:
                    createRsvpLog(event.id, f"Added {user.fullName} to {targetList}.")

        if volunteerExists or rsvpExists:
            return "already in"
    except Exception as e:
        print(e)
        return False

    return True


# ---------------------- Mutual Stuff ----------------------

def addBnumberAsParticipant(bnumber, eventId):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return user and login status"""
    try:
        kioskUser = User.get(User.bnumber == bnumber)
    except Exception as e:
        print(e)
        return None, "does not exist"

    event = Event.get_by_id(eventId)
    if not isEligibleForProgram(event.program, kioskUser):
        userStatus = "banned"

    elif checkUserParticipant(kioskUser, event, False):
        userStatus = "already signed in"

    else:
        userStatus = "success"
        # We are not using addVolunteerToEvent to do this because 
        # that function checks if the event is in the past, but
        # someone could start signing people up via the kiosk
        # before an event has started
        totalHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)
        EventParticipant.create (user=kioskUser, event=event, hoursEarned=totalHours)

    return kioskUser, userStatus

def checkUserParticipant(user,  event, laborCheck):
    if laborCheck == True:
        return EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event == event, EventParticipant.isLabor == True).exists()
    else:
        return EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event == event, EventParticipant.isLabor == False).exists()

# ---------------------- Labor Stuff ----------------------

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

        eventLabor = EventParticipant.get_or_none(user=userObject, event=event)
        checkbox_value = participantData.get(f'checkbox_{username}', 'off')
        didWork = checkbox_value == "on"

        if eventLabor:
            (EventParticipant.update({
                EventParticipant.didWork: didWork
            })
            .where(EventParticipant.event == event.id, EventParticipant.user == userObject.username)
            .execute())
        else:
            EventParticipant.create(
                user=userObject,
                event=event,
                didWork=didWork
            )

    return True

def sortLabor(event):

    eventLabor = getEventParticipants(event, True)

    eventLaborData = eventLabor

    return eventLaborData, eventLabor


def addStudentLaborToEvent(user, event):
    """
        Add a user to an event.
        If the event is in the past, add the user as a volunteer (EventParticipant)
        If the event is in the future, rsvp for the user (EventRsvp)

        Returns True if the operation was successful, false otherwise
    """
    try:
        LaborExists = checkUserParticipant(user, event, True)
        if not LaborExists:
            EventParticipant.create(user=user, event=event, didWork=False, isLabor=True)
        if LaborExists:
            return "already in"
    except Exception as e:
        print(e)
        return False

    return True
    
def addBnumberAsLabor(bnumber, eventId):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return user and login status"""
    try:
        kioskUser = User.get(User.bnumber == bnumber)
    except Exception as e:
        print(e)
        return None, "does not exist"

    event = Event.get_by_id(eventId)
    if not isEligibleForProgram(event.program, kioskUser):
        userStatus = "banned"

    elif checkUserParticipant(kioskUser, event, True):
        userStatus = "already signed in"

    else:
        userStatus = "success"
        EventParticipant.create(user=kioskUser, event=event, didWork=False)

    return kioskUser, userStatus
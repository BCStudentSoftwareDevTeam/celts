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
from app.logic.volunteers import getEventLengthInHours
from app.logic.events import getEventRsvpCountsForTerm
from app.logic.createLogs import createRsvpLog

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

    elif checkUserVolunteer(kioskUser, event):
        userStatus = "already signed in"

    else:
        userStatus = "success"
        # We are not using addPersonToEvent to do this because 
        # that function checks if the event is in the past, but
        # someone could start signing people up via the kiosk
        # before an event has started
        totalHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)
        EventParticipant.create (user=kioskUser, event=event, hoursEarned=totalHours)

    return kioskUser, userStatus

def checkUserRsvp(user,  event):
    return EventRsvp.select().where(EventRsvp.user==user, EventRsvp.event == event).exists()

def checkUserVolunteer(user,  event):
    return EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event == event).exists()

def addPersonToEvent(user, event):
    """
        Add a user to an event.
        If the event is in the past, add the user as a volunteer (EventParticipant) including hours worked.
        If the event is in the future, rsvp for the user (EventRsvp)

        Returns True if the operation was successful, false otherwise
    """
    try:
        volunteerExists = checkUserVolunteer(user, event)
        rsvpExists = checkUserRsvp(user, event)
        if event.isPast:
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


def getEventParticipants(event):
    eventParticipants = (EventParticipant.select(EventParticipant, User)
                                         .join(User)
                                         .where(EventParticipant.event == event))

    return {p.user: p.hoursEarned for p in eventParticipants}

def getParticipationStatusForTrainings(program, userList, term):
    """
    This function returns a dictionary of all trainings for a program and
    whether the current user participated in them.

    :returns: trainings for program and if the user participated
    """
    isRelevantAllVolunteer = (Event.isAllVolunteerTraining) & (Event.term.academicYear == term.academicYear)
    isRelevantProgramTraining = (Event.program == program) & (Event.term == term) & (Event.isTraining)
    programTrainings = (Event.select(Event, Term, EventParticipant, EventRsvp)
                             .join(EventParticipant, JOIN.LEFT_OUTER).switch()
                             .join(EventRsvp, JOIN.LEFT_OUTER).switch()
                             .join(Term)
                             .where(isRelevantAllVolunteer | isRelevantProgramTraining, (Event.isCanceled != True)).order_by(Event.startDate))

    # Create a dictionary where the keys are trainings and values are a list of those who attended
    trainingData = {}
    for training in programTrainings:
        try:
            if training.isPast:
                trainingData[training] = trainingData.get(training, []) + [training.eventparticipant.user_id]
            else:  # The training has yet to happen
                trainingData[training] = trainingData.get(training, []) + [training.eventrsvp.user_id]
        except AttributeError:
            trainingData[training] = trainingData.get(training, [])
    # Create a dictionary binding usernames to tuples. The tuples consist of the training (event object) and whether or not they attended it (bool)
    userParticipationStatus = {}
    for user in userList:
        for training, attendeeList in trainingData.items():
            userParticipationStatus[user.username] = userParticipationStatus.get(user.username, []) + [(training, user.username in attendeeList)]

    return userParticipationStatus

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

def trainedParticipants(programID, currentTerm):
    """
    This function tracks the users who have attended every Prerequisite
    event and adds them to a list that will not flag them when tracking hours.
    """

    academicYear = currentTerm.academicYear

    # Reset program eligibility each term for all other trainings

    otherTrainingEvents = (Event.select(Event.id)
            .join(Term)
            .where(
                Event.program == programID,
                (Event.isTraining | Event.isAllVolunteerTraining),
                Event.term.academicYear == academicYear)
            )

    allTrainingEvents = set(otherTrainingEvents)
    eventTrainingDataList = [participant.user for participant in (
        EventParticipant.select().where(EventParticipant.event.in_(allTrainingEvents))
        )]
    attendedTraining = list(dict.fromkeys(filter(lambda user: eventTrainingDataList.count(user) == len(allTrainingEvents), eventTrainingDataList)))
    return attendedTraining

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

def getUserParticipatedTrainingEvents(program, user, currentTerm):
    """
    This function returns a dictionary of all trainings for a program and
    whether the current user participated in them.

    :returns: trainings for program and if the user participated
    """
    academicYear = currentTerm.academicYear

    programTrainings = (Event.select(Event, Term, EventParticipant)
                               .join(EventParticipant, JOIN.LEFT_OUTER).switch()
                               .join(Term)
                               .where((Event.isTraining | Event.isAllVolunteerTraining),
                                      Event.program== program,
                                      Event.term.academicYear == academicYear,
                                      EventParticipant.user.is_null(True) | (EventParticipant.user == user)))

    UserParticipatedTrainingEvents = {}
    for training in programTrainings.objects():
        if training.startDate > date.today():
            didParticipate = [None, training.startDate.strftime("%m/%d/%Y")]
        elif training.user:
            didParticipate = True
        else:
            didParticipate = False
        UserParticipatedTrainingEvents[training.name] = didParticipate
    return UserParticipatedTrainingEvents

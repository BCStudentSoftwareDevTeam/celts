from peewee import fn
from app.models.user import User
from app.models.event import Event
from app.models.eventRsvp import EventRsvp
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.eventParticipant import EventParticipant
from app.logic.users import isEligibleForProgram
from app.logic.volunteers import getEventLengthInHours

def trainedParticipants(programID, currentTerm):
    """
    This function tracks the users who have attended every Prerequisite
    event and adds them to a list that will not flag them when tracking hours.
    """
    # programId = 3
    # events = 3, 6, 10, 12
    # 10 - All celts training

    #trainingEvents = [3, 6, 10]

    # exclude events with name All celts training and All volunteer training
    trainingEvents = list(Event.select()
                               .join(ProgramEvent)
                               .where(ProgramEvent.program==programID, Event.isTraining==True, Event.term==currentTerm))


    # Exception for All Celts training and All volunteer training
    # if 10 in trainingEvents and (if user and 10 is in EventParticipant)
    # [3, 6, 10] - [10]

    #term term.academicYear "2021-2022"
    # isInCurrentAcademicYear = if (fall in term.description and term.year in term.academicYear[everything-before-dash])   term.academicYear.split("-")[0]




    eventTrainingDataList = [participant.user.username for participant in (
        EventParticipant.select().where(EventParticipant.event.in_(trainingEvents))
        )]

    attendedTraining = list(dict.fromkeys(filter(lambda user: eventTrainingDataList.count(user) == len(trainingEvents), eventTrainingDataList)))
    return attendedTraining

def sendUserData(bnumber, eventId, programid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return user and login status"""
    signedInUser = User.get(User.bnumber == bnumber)
    event = Event.get_by_id(eventId)
    if not isEligibleForProgram(programid, signedInUser):
        userStatus = "banned"
    elif ((EventParticipant.select(EventParticipant.user)
       .where(EventParticipant.user==signedInUser, EventParticipant.event==eventId))
       .exists()):
        userStatus = "already in"
    else:
        userStatus = "success"
        totalHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)
        EventRsvp.create(user=signedInUser, event=eventId)
        EventParticipant.create (user=signedInUser, event=eventId, hoursEarned=totalHours)
    return signedInUser, userStatus

def userRsvpForEvent(user,  event):
    """
    Lets the user RSVP for an event if they are eligible and creates an entry for them in the EventParticipant table.

    :param user: accepts a User object or username
    :param event: accepts an Event object or a valid event ID
    :return: eventParticipant entry for the given user and event; otherwise raise an exception
    """

    rsvpUser = User.get_by_id(user)
    rsvpEvent = Event.get_by_id(event)
    program = Program.select(Program).join(ProgramEvent).where(ProgramEvent.event == event).get()

    isEligible = isEligibleForProgram(program, user)
    if isEligible:
        newParticipant = EventRsvp.get_or_create(user = rsvpUser, event = rsvpEvent)[0]
        return newParticipant
    return isEligible



def unattendedRequiredEvents(program, user):

    # Check for events that are prerequisite for program
    requiredEvents = (Event.select(Event)
                           .join(ProgramEvent)
                           .where(Event.isTraining == True, ProgramEvent.program == program))

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
    eventParticipants = (EventParticipant
        .select()
        .where(EventParticipant.event==event))

    return {p.user.username: p.hoursEarned for p in eventParticipants}

from peewee import fn
from app.models.user import User
from app.models.event import Event
from app.models.term import Term
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

    ayStart = currentTerm.academicYearStartingTerm

    # Reset program eligibility each term for all other trainings

    otherTrainingEvents = (Event.select(Event.id).join(ProgramEvent)
            .where(
                ProgramEvent.program==programID,
                Event.isTraining==True,
                (((Event.name == "All Celts Training") | (Event.name == "All Volunteer Training")) & (Event.term == ayStart)) | (Event.term==currentTerm))
            )

    allTraningEvents = set(otherTrainingEvents)

    eventTrainingDataList = [participant.user.username for participant in (
        EventParticipant.select().where(EventParticipant.event.in_(allTraningEvents))
        )]

    attendedTraining = list(dict.fromkeys(filter(lambda user: eventTrainingDataList.count(user) == len(allTraningEvents), eventTrainingDataList)))
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

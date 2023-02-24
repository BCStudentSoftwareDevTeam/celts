from peewee import fn, JOIN
import datetime
from datetime import date
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

    academicYear = currentTerm.academicYear

    # Reset program eligibility each term for all other trainings

    otherTrainingEvents = (Event.select(Event.id)
            .join(ProgramEvent).switch()
            .join(Term)
            .where(
                ProgramEvent.program == programID,
                (Event.isTraining | Event.isAllVolunteerTraining),
                Event.term.academicYear == academicYear)
            )

    allTrainingEvents = set(otherTrainingEvents)
    eventTrainingDataList = [participant.user for participant in (
        EventParticipant.select().where(EventParticipant.event.in_(allTrainingEvents))
        )]
    attendedTraining = list(dict.fromkeys(filter(lambda user: eventTrainingDataList.count(user) == len(allTrainingEvents), eventTrainingDataList)))
    return attendedTraining

def sendUserData(bnumber, eventId, programid):
    """Accepts scan input and signs in the user. If user exists or is already
    signed in will return user and login status"""
    try:
        signedInUser = User.get(User.bnumber == bnumber)
    except Exception as e:
        print(e)
        return None, "does not exist"
    event = Event.get_by_id(eventId)
    if not isEligibleForProgram(programid, signedInUser):
        userStatus = "banned"
    elif ((EventParticipant.select(EventParticipant.user)
       .where(EventParticipant.user == signedInUser, EventParticipant.event==eventId))
       .exists()):
        userStatus = "already in"
    else:
        userStatus = "success"
        totalHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)
        EventParticipant.create (user=signedInUser, event=eventId, hoursEarned=totalHours)
    return signedInUser, userStatus

def checkUserRsvp(user,  event):
    participantRSvp = EventRsvp.get_or_none(EventRsvp.user==user, EventRsvp.event == event)
    #if there's no EventRSVP record, student has not rsvp
    if participantRSvp is not None: 
        if participantRSvp.unRsvpTime is not None: #if rsvp record exists and unrsvp is not None
            if participantRSvp.unRsvpTime > participantRSvp.rsvpTime:
                return False
            else:
                return True 
        else: 
#if there's a record and unRsvptime is none, rsvp is true
            return True
    else:    
        return False

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
        print("HEREEEEE RSVP exists", type(rsvpExists))
        print(event.isPast)
        if event.isPast:
            if not volunteerExists:
                eventHours = getEventLengthInHours(event.timeStart, event.timeEnd, event.startDate)
                EventParticipant.create(user = user, event = event, hoursEarned = eventHours)
        else:
            print("Not past event")
            # Adding RSVP if the person has rsvp before 
            if rsvpExists == False: 
                if EventRsvp.select().where(EventRsvp.user == user, EventRsvp.event == event).exists():
                    print("HEREEEEEEEEEEEEEEEEEE to RSVP after unrsvp")
                    EventRsvp.update({EventRsvp.rsvpTime: datetime.datetime.now()}).where(EventRsvp.user == user, EventRsvp.event == event).execute()
                    print("Have already updated!")
                else:
                    EventRsvp.create(user = user, event = event)

        if volunteerExists or rsvpExists:
            return "already in"
    except Exception as e:
        print(e)
        return False

    return True

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

    programTrainings = (Event.select(Event, ProgramEvent, Term, EventParticipant)
                               .join(EventParticipant, JOIN.LEFT_OUTER).switch()
                               .join(ProgramEvent).switch()
                               .join(Term)
                               .where((Event.isTraining | Event.isAllVolunteerTraining),
                                      ProgramEvent.program == program,
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

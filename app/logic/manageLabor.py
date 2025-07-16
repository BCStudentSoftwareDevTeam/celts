from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.logic.users import isEligibleForProgram

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

def getLaborStudents(event):
    eventLabor = (EventParticipant.select(EventParticipant, User)
                                         .join(User)
                                         .where((EventParticipant.event == event) & (EventParticipant.isLabor == True)))

    return [p for p in eventLabor]



def sortLabor(event):

    eventLabor = getLaborStudents(event)

    eventLaborData = eventLabor

    return eventLaborData, eventLabor

def checkUserLabor(user,  event):
    return EventParticipant.select().where(EventParticipant.user == user, EventParticipant.event == event, EventParticipant.isLabor == True).exists()


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

    elif checkUserLabor(kioskUser, event):
        userStatus = "already signed in"

    else:
        userStatus = "success"
        EventParticipant.create(user=kioskUser, event=event, didWork=False)

    return kioskUser, userStatus
import pytest
from app.models.user import User
from app.logic.userRsvpForEvent import userRsvpForEvent, unattendedRequiredEvents
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from peewee import DoesNotExist

@pytest.mark.integration
def test_notUserRsvpForEvent():

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("asdkl", 1)

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent(132546, 1)

@pytest.mark.integration
def test_noEventUserRsvpForEvent():

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", 1500)

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", "Event")

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", -1)

    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("khatts", 0)


@pytest.mark.integration
def test_userRsvpForEvent():

    volunteer = userRsvpForEvent("agliullovak", 11)
    assert volunteer.user.username == "agliullovak"
    assert volunteer.event.id == 11
    assert volunteer.rsvp == True

    # the user has already registered for the event
    volunteer = userRsvpForEvent("agliullovak", 11)
    assert volunteer.event.id == 11
    assert volunteer

    (EventParticipant.delete().where(EventParticipant.user == 'agliullovak', EventParticipant.event == 11)).execute()

    # the user is not eligible to register (reason: user is banned)
    volunteer = userRsvpForEvent("ayisie", 1)
    assert volunteer == False

    # User does not exist
    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("jarjug", 2)

    #program does not exist
    with pytest.raises(DoesNotExist):
        volunteer = userRsvpForEvent("agliullovak", 500)

# tests for unattendedRequiredEvents
@pytest.mark.integration
def test_unattendedRequiredEvents():

    # test unattended events
    program = 1
    user = 'ramsayb2'

    unattendedEvents = unattendedRequiredEvents(program, user)
    assert len(unattendedEvents) == 3

    # test after user has attended an event
    event = Event.get(Event.eventName == unattendedEvents[0])
    EventParticipant.create(user = user, event = event, attended = True)
    unattendedEvents = unattendedRequiredEvents(program, user)
    assert len(unattendedEvents) == 2
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == event)).execute()

    # test where all required events are attended
    user = 'khatts'
    unattendedEvents = unattendedRequiredEvents(program, user)
    assert unattendedEvents == []

    # test for program with no requirements
    program = 4
    unattendedEvents = unattendedRequiredEvents(program, user)
    assert unattendedEvents == []


    # test for incorrect program
    program = 500
    unattendedEvents = unattendedRequiredEvents(program, user)
    assert unattendedEvents == []

    #test for incorrect user
    program = 1
    user = "asdfasdf56"
    unattendedEvents = unattendedRequiredEvents(program, user)
    assert unattendedEvents == ['Empty Bowls Spring', 'Berea Buddies', 'How To Make Buddies']

import pytest
from datetime import datetime
from peewee import IntegrityError, DoesNotExist

from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.logic.volunteers import addVolunteerToEvent
from app.logic.participants import trainedParticipants
from app.logic.volunteers import getEventLengthInHours, updateVolunteers
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents
from app.logic.participants import sendUserData
from app.models.eventRsvp import EventRsvp

@pytest.mark.integration
def test_getEventLengthInHours():
    #test for correct time in hours

    startTime = datetime.strptime("15:00:37", "%H:%M:%S").time()
    endTime = datetime.strptime("18:00:39", "%H:%M:%S").time()
    eventDate = datetime.strptime("2021-07-20", "%Y-%m-%d")
    eventLength = getEventLengthInHours(startTime, endTime, eventDate)
    assert eventLength == 3

    #input type is datetime object and only minutes and hours
    endTime = datetime.strptime("18:40", "%H:%M").time()
    eventLength = getEventLengthInHours(startTime, endTime, eventDate)
    assert eventLength == 3.66

    startTime = datetime.strptime("16:05", "%H:%M").time()
    endTime = datetime.strptime("18:40", "%H:%M").time()
    eventLength = getEventLengthInHours(startTime, endTime, eventDate)
    assert eventLength == 2.58

    # input type is datetime instead of time
    startTime = datetime.strptime("16:05", "%H:%M")

    with pytest.raises(TypeError):
        eventLength = getEventLengthInHours(startTime, endTime, eventDate)

    #input type is string instead of time
    startTime = "16:05"
    with pytest.raises(TypeError):
        eventLength = getEventLengthInHours(startTime, endTime, eventDate)

    #input type is string instead of datetime
    startTime = datetime.strptime("16:05", "%H:%M").time()
    eventDate = "2021-07-20"
    with pytest.raises(TypeError):
        eventLength = getEventLengthInHours(startTime, endTime, eventDate)



@pytest.mark.integration
def test_addVolunteerToEvent():
    user = "khatts"
    volunteerEventID = 5
    eventLengthInHours = 67
    #test that volunteer is already registered for the event
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == True

    #test for adding user as a participant to the event
    user = "agliullovak"
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == True
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == volunteerEventID)).execute()

    # test for username that is not in the database
    user = "jarjug"
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == False

    # test for event that does not exsit
    user = "agliullovak"
    volunteerEventID = 5006
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == False


@pytest.mark.integration
def test_updateVolunteers():
    # tests if the volunteer table gets succesfully updated
    participantData = {'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateVolunteers(participantData)
    assert volunteerTableUpdate == True

    # tests if user does not exist in the database
    participantData = {'inputHours_jarjug':100, 'checkbox_jarjug':"on", 'event':3, 'username1': 'jarjug'}
    volunteerTableUpdate = updateVolunteers(participantData)
    assert volunteerTableUpdate == False

    # tests for the case when the checkbox is not checked (user is not present)
    participantData = {'inputHours_agliullovak':100, 'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateVolunteers(participantData)
    assert volunteerTableUpdate == True

    #Undo the above test changes
    participantData = {'inputHours_agliullovak':2, 'checkbox_agliullovak':"on", 'event':3, 'username1': 'agliullovak'}

@pytest.mark.integration
def test_trainedParticipants():
    attendedPreq = trainedParticipants(1)
    assert "neillz" and "khatts" in attendedPreq

    #test for program with no prereq
    attendedPreq = trainedParticipants(4)
    assert attendedPreq == []

    #test for program that doesn't exist
    attendedPreq = trainedParticipants(500)
    assert attendedPreq == []

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

    volunteer = userRsvpForEvent("agliullovak", 10)
    assert volunteer.user.username == "agliullovak"
    assert volunteer.event.id == 10


    # the user has already registered for the event
    volunteer = userRsvpForEvent("agliullovak", 10)
    assert volunteer.event.id == 10
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
    event = Event.get(Event.name == unattendedEvents[0])
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
    assert unattendedEvents == ['Empty Bowls Spring Event 1', 'Berea Buddies Training', 'How To Make Buddies']

@pytest.mark.integration
def test_sendKioskDataKiosk():
    # user is banned
    signedInUser, userStatus = sendUserData("B00739736", 2, 1)
    assert userStatus == "banned"

    with pytest.raises(DoesNotExist):
        EventParticipant.get(EventParticipant.user==signedInUser, EventParticipant.event==2)

    # user is already signed in
    signedInUser, userStatus = sendUserData("B00751360", 2, 1)
    assert userStatus == "already in"

    # user is eligible but the user is not in EventParticipant
    signedInUser = User.get(User.bnumber=="B00759117")
    with pytest.raises(DoesNotExist):
        EventParticipant.get(EventParticipant.user==signedInUser, EventParticipant.event==2)

    signedInUser, userStatus = sendUserData("B00759117", 2, 1)
    assert userStatus == "success"

    usersAttended = EventParticipant.select().where(EventParticipant.event == 2)
    listOfAttended = [users.user.username for users in usersAttended]

    assert "agliullovak" in listOfAttended

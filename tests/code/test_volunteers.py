import pytest
from app.logic.volunteers import getEventLengthInHours, updateEventParticipants
from app.models.eventParticipant import EventParticipant
from app.controllers.admin.volunteers import addVolunteerToEventRsvp
from datetime import datetime
from peewee import DoesNotExist


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
def test_addVolunteerToEventRsvp():
    user = "khatts"
    volunteerEventID = 5
    #test that volunteer is already registered for the event
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID)
    assert volunteerToEvent == True

    #test for adding user as a participant to the event
    user = "agliullovak"
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID)
    assert volunteerToEvent == True
    (EventParticipant.delete().where(EventParticipant.user==user, EventParticipant.event==volunteerEventID)).execute()

    # test for username that is not in the database
    user = "jarjug"
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID)
    assert volunteerToEvent == False

    # test for event that does not exsit
    user = "agliullovak"
    volunteerEventID = 5006
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID)
    assert volunteerToEvent == False


@pytest.mark.integration
def test_updateEventParticipants():
    # event does not exist
    participantData = {'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':100, 'username1': 'agliullovak'}
    with pytest.raises(Exception, match="Event does not exist."):
        volunteerTableUpdate = updateEventParticipants(participantData)
        assert volunteerTableUpdate == False

    # update record if user is marked as present and user record exists in event participant table
    participantData = {'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    eventParticipant = EventParticipant.get(EventParticipant.user=="agliullovak", EventParticipant.event==3)
    assert eventParticipant.hoursEarned == 100

    # create new record if user is marked present but doesn't have a record in event participant table
    with pytest.raises(DoesNotExist):
        EventParticipant.get(EventParticipant.user=="partont", EventParticipant.event==3)

    participantData = {'inputHours_partont':100, 'checkbox_partont':"on", 'event':3, 'username1': 'partont'}
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    eventParticipant = EventParticipant.get(EventParticipant.user=="partont", EventParticipant.event==3)
    assert eventParticipant.hoursEarned == 100

    ((EventParticipant.delete()
        .where(EventParticipant.user=="partont", EventParticipant.event==3))
        .execute())

    # delete user from event participant table if user is marked absent and they have a record in the table
    participantData = {'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    with pytest.raises(DoesNotExist):
        EventParticipant.get(EventParticipant.user=="agliullovak", EventParticipant.event==3)

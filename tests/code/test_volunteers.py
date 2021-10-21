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
    eventLengthInHours = 67
    #test that volunteer is already registered for the event
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == True

    #test for adding user as a participant to the event
    user = "agliullovak"
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == True
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == volunteerEventID)).execute()

    # test for username that is not in the database
    user = "jarjug"
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == False

    # test for event that does not exsit
    user = "agliullovak"
    volunteerEventID = 5006
    volunteerToEvent = addVolunteerToEventRsvp(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == False


@pytest.mark.integration
def test_updateEventParticipants():
    # TODO: test update, create, delete
    # tests the checkbox is checked and user exdists in EventParticipant, then updates the record
    participantData = {'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    # tests if the checkbox is not checked and user is not in EventParticipant, then delete a record
    with pytest.raises(DoesNotExist):
        updateEventParticipants(participantData)

    # tests if the checkbox is checked and user is not in EventParticipant, then create a new entry

    # tests for the case when the checkbox is not checked (user is not present)
    participantData = {'inputHours_agliullovak':100, 'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    #Undo the above test changes
    participantData = {'inputHours_agliullovak':2, 'checkbox_agliullovak':"on", 'event':3, 'username1': 'agliullovak'}

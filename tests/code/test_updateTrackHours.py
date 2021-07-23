import pytest
from app.logic.updateTrackHours import getEventLengthInHours, addVolunteerToEvent, updateTrackHours
from app.models.eventParticipant import EventParticipant
from datetime import datetime


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
    assert volunteerToEvent == "Volunteer already exists."

    #test for adding user as a participant to the event
    user = "agliullovak"
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == "Volunteer successfully added!"
    (EventParticipant.delete().where(EventParticipant.user == user, EventParticipant.event == volunteerEventID)).execute()

    # test for username that is not in the database
    user = "jarjug"
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == ("Error when adding volunteer", 500)

    # test for event that does not exsit
    user = "agliullovak"
    volunteerEventID = 5006
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID, eventLengthInHours)
    assert volunteerToEvent == ("Error when adding volunteer", 500)


@pytest.mark.integration
def test_updateTrackHours():
    # tests if the volunteer table gets succesfully updated
    participantData = {'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':3, 'username1': 'agliullovak'}
    volunteerTableUpdate = updateTrackHours(participantData)
    assert volunteerTableUpdate == "Volunteer table successfully updated!"

    # tests if user does not exist in the database
    participantData = {'inputHours_jarjug':100, 'checkbox_jarjug':"on", 'event':3, 'username1': 'jarjug'}
    volunteerTableUpdate = updateTrackHours(participantData)
    assert volunteerTableUpdate ==  "Volunteer does not exist."

    # tests for the case when the checkbox is not checked (user is not present)
    participantData = {'inputHours_ramsayb2':100, 'event':3, 'username1': 'ramsayb2'}
    volunteerTableUpdate = updateTrackHours(participantData)
    assert volunteerTableUpdate == "Volunteer table successfully updated!"

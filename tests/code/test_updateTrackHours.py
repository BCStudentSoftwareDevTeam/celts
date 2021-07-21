import pytest
from app.logic.updateTrackHours import eventLengthInHours, addVolunteerToEvent, updateTrackHours
from datetime import datetime


@pytest.mark.integration
def test_eventLengthInHours():
    #test for correct time in hours

    startTime = datetime.strptime("15:00:37", "%H:%M:%S").time()
    endTime = datetime.strptime("18:00:39", "%H:%M:%S").time()
    eventDate = datetime.strptime("2021-07-20", "%Y-%m-%d")
    eventLength = eventLengthInHours(startTime, endTime, eventDate)
    assert eventLength == 3

    #input type is datetime object and only minutes and hours
    endTime = datetime.strptime("18:40", "%H:%M").time()
    eventLength = eventLengthInHours(startTime, endTime, eventDate)
    assert eventLength == 3.65

    startTime = datetime.strptime("16:05", "%H:%M").time()
    endTime = datetime.strptime("18:40", "%H:%M").time()
    eventLength = eventLengthInHours(startTime, endTime, eventDate)
    assert eventLength == 2.58

    # input type is datetime instead of time
    startTime = datetime.strptime("16:05", "%H:%M")

    with pytest.raises(TypeError):
        eventLength = eventLengthInHours(startTime, endTime, eventDate)

    #input type is string instead of time
    startTime = "16:05"
    with pytest.raises(TypeError):
        eventLength = eventLengthInHours(startTime, endTime, eventDate)

    #input type is string instead of datetime
    startTime = datetime.strptime("16:05", "%H:%M").time()
    eventDate = "2021-07-20"
    with pytest.raises(TypeError):
        eventLength = eventLengthInHours(startTime, endTime, eventDate)



@pytest.mark.integration
def test_addVolunteerToEvent():
    print("=================")
    user = "khatts"
    volunteerEventID = 5
    volunteerToEvent = addVolunteerToEvent(user, volunteerEventID)
    assert volunteerToEvent == "Volunteer already exists."




@pytest.mark.integration
def test_updateTrackHours():
    pass

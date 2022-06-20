import pytest
from flask import g
from app import app
from app.logic.volunteers import getEventLengthInHours, updateEventParticipants, setUserBackgroundCheck, getProgramManagerForEvent
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.controllers.admin.volunteers import addVolunteerToEventRsvp
from app.models.backgroundCheck import BackgroundCheck
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

@pytest.mark.integration
def test_backgroundCheck():
    with app.app_context():
        g.current_user = "ramsayb2"
        updatebackground = setUserBackgroundCheck("khatts","CAN",False)
        updatedModel = BackgroundCheck.get(user="khatts", type = "CAN")
        assert updatedModel.passBackgroundCheck == False

        updatebackground = setUserBackgroundCheck("khatts","FBI",True)
        updatedModel = BackgroundCheck.get(user =  "khatts", type = "FBI")
        assert updatedModel.passBackgroundCheck == True

        updatebackground = setUserBackgroundCheck("khatts","SHS",False)
        updatedModel = BackgroundCheck.get(user = "khatts", type = "SHS")
        assert updatedModel.passBackgroundCheck == False

        updatebackground = setUserBackgroundCheck("neillz", "FBI",False)
        updatedModel = BackgroundCheck.get(user =  "neillz", type = "FBI")
        assert updatedModel.passBackgroundCheck == False

        updatebackground = setUserBackgroundCheck("mupotsal","SHS",True)
        updatedModel = BackgroundCheck.get(user = "mupotsal", type = "SHS")
        assert updatedModel.passBackgroundCheck == True

@pytest.mark.integration
def test_getStudentManagerForEvent():
    with app.app_context():
        testData = [
        {
        "id":13,
        "programName":"testName",
        "isStudentLed": False,
        "isBonnerScholars":False,
        }
        ]
        Program.insert_many(testData).on_conflict_replace().execute()

        testEvent = [
        {
        "id": 16,
        "term": 2,
        "name": "testEvent",
        "description": "testEvent",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Seabury Center",
        "startDate": datetime.strptime("2021 10 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
        }
        ]
        Event.insert_many(testEvent).on_conflict_replace().execute()

        testProgramEvent = [
        {
        "program_id":13,
        "event_id":16,
        }
        ]
        #ProgramEvent.insert_many(testProgramEvent).on_conflict_replace().execute()

        #gives event & programID
        ## user is manager of program
        student = User.get_by_id("neillz")
        event = Event.get_by_id(1)
        studentManager = getProgramManagerForEvent(student, event, 1)
        assert studentManager == True
        ## user is not manager of program
        student = User.get_by_id("khatts")
        event = Event.get_by_id(1)
        studentManager = getProgramManagerForEvent(student, event, 5)
        assert studentManager == False

        #gives event but no programId
        ## user is manager of program
        student = User.get_by_id("khatts")
        event = Event.get_by_id(1)
        studentManager = getProgramManagerForEvent(student, event)
        assert studentManager == True
        ## user is not manager of program
        student = User.get_by_id("khatts")
        event = Event.get_by_id(5)
        studentManager = getProgramManagerForEvent(student, event, 5)
        assert studentManager == False

        #gives programID but no event
        ## user is manager of program
        student = User.get_by_id("neillz")
        event = Event.get_by_id(1)
        studentManager = getProgramManagerForEvent(student, programId = 1)
        assert studentManager == True
        ## user is not manager of program
        student = User.get_by_id("partont")
        event = Event.get_by_id(1)
        studentManager = getProgramManagerForEvent(student, programId = 5)
        assert studentManager == False

        #gives neither event or programID
        ## shuold give an error, most likely a 500: system error
        # student = User.get_by_id("neillz")
        # event = Event.get_by_id(None)
        with pytest.raises(ValueError):
            # EventParticipant.get(EventParticipant.user=="agliullovak", EventParticipant.event==3)
            studentManager = getProgramManagerForEvent(student)
        # assert studentManager == False # use different assertion for errors handling?
        Program.get(Program.id==13).delete_instance()
        Event.get(Event.id==16).delete_instance()
        #ProgramEvent.get(ProgramEvent.event_id==13).delete_instance()

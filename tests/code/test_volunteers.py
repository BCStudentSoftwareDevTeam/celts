import pytest
from flask import g
from app import app
from app.logic.volunteers import getEventLengthInHours, updateEventParticipants, setUserBackgroundCheck, isProgramManagerForEvent
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from app.models.program import Program
from app.models.studentManager import StudentManager
from app.models.programEvent import ProgramEvent
from app.models import mainDB
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
        assert updatedModel.dateCompleted.strftime("%Y-%m-%d") == "2021-07-20"

@pytest.mark.integration
def test_getStudentManagerForEvent():
    with mainDB.atomic() as transaction:

        #Test data for creating a program
        testProgramData = [
        {
        "id":13,
        "programName":"testProgram",
        "isStudentLed": False,
        "isBonnerScholars":False,
        }
        ]

        #Inserts new row into Program table
        Program.insert_many(testProgramData).on_conflict_replace().execute()

        #Test data for creating an event
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

        Event.insert_many(testEvent).on_conflict_replace().execute() #Inserts new row into Event table

        #Test data for creating a new row in ProgramEvent table
        testProgramEvent = [
        {
        "program_id":13,
        "event_id":16,
        }
        ]

        #Inserts new row into ProgramEvent table
        ProgramEvent.insert_many(testProgramEvent).on_conflict_replace().execute()

        #Test data for test users, inserted in User table
        testUserData = [
        {#This user is not a program manager
        "username": "testUser",
        "bnumber": "B00724094",
        "email": "martinj2@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Joey",
        "lastName": "Martin",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False

        },
        {#This user is a program manager
        "username": "testUser2",
        "bnumber": "B00762158",
        "email": "studentmanagertest@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Paw",
        "lastName": "Thaw",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": True
        }
        ]

        #Insert new row into User table
        User.insert_many(testUserData).on_conflict_replace().execute()

        #Test data for StudentManager table, inserted in to StudentManager table
        testProgramManagerData = [
        {
        'user': 'testUser2',
        'program': 13
        }
        ]

        #Insert new row into StudentManager table
        StudentManager.insert_many(testProgramManagerData).on_conflict_replace().execute()

        test_program = 13 #programID is passed in  as an int
        test_event = Event.get_by_id(16) #gets event object
        student = User.get_by_id("testUser") #This test user is not a program manager
        programManager = User.get_by_id("testUser2") ##This user is a program manager



        ## user is manager of program
        studentManager = isProgramManagerForEvent(programManager, test_event)
        assert studentManager == True

        ## user is not manager of program
        studentManager = isProgramManagerForEvent(student, test_event)
        assert studentManager == False



        transaction.rollback()

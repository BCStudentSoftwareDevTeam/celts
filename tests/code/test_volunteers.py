import pytest
from flask import g
from werkzeug.datastructures import ImmutableMultiDict
from app import app
from app.logic.volunteers import getEventLengthInHours, updateEventParticipants, addUserBackgroundCheck, sortParticipantsByStatus
from app.models.eventParticipant import EventParticipant
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models.event import Event
from app.models.program import Program
from app.models.programManager import ProgramManager
from app.models import mainDB
from app.models.backgroundCheck import BackgroundCheck
from datetime import datetime
from peewee import DoesNotExist
from dateutil import parser


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
def test_updateEventParticipants():
    with mainDB.atomic() as transaction:
        # event does not exist
        participantData = ImmutableMultiDict({'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':100, 'username': 'agliullovak'})
        with pytest.raises(Exception, match="Event does not exist."):
            volunteerTableUpdate = updateEventParticipants(participantData)
            assert volunteerTableUpdate == False

        # update record if user is marked as present and user record exists in event participant table
        participantData = ImmutableMultiDict({'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':3, 'username': 'agliullovak'})
        volunteerTableUpdate = updateEventParticipants(participantData)
        assert volunteerTableUpdate == True

        eventParticipant = EventParticipant.get(EventParticipant.user=="agliullovak", EventParticipant.event==3)
        assert eventParticipant.hoursEarned == 100

        # create new record if user is marked present but doesn't have a record in event participant table
        with pytest.raises(DoesNotExist):
            EventParticipant.get(EventParticipant.user=="partont", EventParticipant.event==3)


        # add two users with hours
        participantData = ImmutableMultiDict([('inputHours_partont', 100), ('checkbox_partont', "on"), ('event', 3), ('username', 'partont'), ('username', 'neillz'), ('inputHours_neillz', 75), ('checkbox_neillz', "on")])
        volunteerTableUpdate = updateEventParticipants(participantData)
        assert volunteerTableUpdate == True

        # check that users were added
        eventParticipant = EventParticipant.get(EventParticipant.user=="neillz", EventParticipant.event==3)
        assert eventParticipant.hoursEarned == 75
        eventParticipant = EventParticipant.get(EventParticipant.user=="partont", EventParticipant.event==3)
        assert eventParticipant.hoursEarned == 100

        # remove neillz, partont unchanged
        participantData = ImmutableMultiDict([('inputHours_partont', 100), ('checkbox_partont', "on"), ('event', 3), ('username', 'partont'), ('username', 'neillz')])
        volunteerTableUpdate = updateEventParticipants(participantData)
        assert volunteerTableUpdate == True

        # check that neillz was removed and partont remained the same
        eventParticipant = EventParticipant.get_or_none(EventParticipant.user=="neillz", EventParticipant.event==3)
        assert eventParticipant == None
        eventParticipant = EventParticipant.get(EventParticipant.user=="partont", EventParticipant.event==3)
        assert eventParticipant.hoursEarned == 100

        ((EventParticipant.delete()
            .where(EventParticipant.user=="partont", EventParticipant.event==3))
            .execute())

        # delete user from event participant table if user is marked absent and they have a record in the table
        participantData = ImmutableMultiDict({'event':3, 'username': 'agliullovak'})
        volunteerTableUpdate = updateEventParticipants(participantData)
        assert volunteerTableUpdate == True

        with pytest.raises(DoesNotExist):
            EventParticipant.get(EventParticipant.user=="agliullovak", EventParticipant.event==3)

        transaction.rollback()

@pytest.mark.integration
def test_backgroundCheck():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = "ramsayb2"
            # tests the model created in tests_data and the one that is created (multiple entries)
            updatebackground = addUserBackgroundCheck("khatts","CAN","Submitted",parser.parse("2020-07-20"))
            updatedModel = list(BackgroundCheck.select().where(BackgroundCheck.user == "khatts", BackgroundCheck.type == "CAN"))
            assert updatedModel[0].backgroundCheckStatus == "Passed"
            assert updatedModel[1].backgroundCheckStatus == "Submitted"
            assert updatedModel[0].dateCompleted.strftime("%Y-%m-%d") == "2021-10-12"
            assert updatedModel[1].dateCompleted.strftime("%Y-%m-%d") == "2020-07-20"

            updatebackground = addUserBackgroundCheck("mupotsal","SHS","Failed",parser.parse("2021-07-20"))
            updatedModel = list(BackgroundCheck.select().where(BackgroundCheck.user == "mupotsal", BackgroundCheck.type == "SHS"))
            assert updatedModel[0].backgroundCheckStatus == "Submitted"
            assert updatedModel[1].backgroundCheckStatus == "Failed"
            assert updatedModel[0].dateCompleted.strftime("%Y-%m-%d") == "2021-10-12"
            assert updatedModel[1].dateCompleted.strftime("%Y-%m-%d") == "2021-07-20"

            # tests the creation of adding a new background check where one does not exist yet
            updatebackground = addUserBackgroundCheck("khatts","FBI","Passed",parser.parse("1999-07-20"))
            updatedModel = BackgroundCheck.get(user =  "khatts", type = "FBI")
            assert updatedModel.backgroundCheckStatus == "Passed"
            assert updatedModel.dateCompleted.strftime("%Y-%m-%d") == "1999-07-20"


            updatebackground = addUserBackgroundCheck("khatts","SHS","Submitted",parser.parse("2019-07-20"))
            updatedModel = BackgroundCheck.get(user = "khatts", type = "SHS")
            assert updatedModel.backgroundCheckStatus == "Submitted"
            assert updatedModel.dateCompleted.strftime("%Y-%m-%d") == "2019-07-20"

            updatebackground = addUserBackgroundCheck("neillz", "FBI","Passed",parser.parse("2009-07-20"))
            updatedModel = BackgroundCheck.get(user =  "neillz", type = "FBI")
            assert updatedModel.backgroundCheckStatus == "Passed"
            assert updatedModel.dateCompleted.strftime("%Y-%m-%d") == "2009-07-20"

        transaction.rollback()

@pytest.mark.integration
def test_sortParticipantsByStatus():
    """
    Test the sorting of event participants into the 
    non attended, waitlist, and attended groups.
    """
    with mainDB.atomic() as transaction:
        
        # creating past event
        testingEvent = Event.create(name = "Testing event",
                                    term = 3,
                                    description = "This Event is Created to be tested.",
                                    timeStart = "07:00 PM",
                                    timeEnd = "10:00 PM",
                                    location = "Somewhere",
                                    isRsvpRequired = 0,
                                    isTraining = 0,
                                    isService = 0,
                                    startDate = "2021-12-12",
                                    endDate = "2022-6-12",
                                    isCanceled = False,
                                    program = 2)
        

        EventParticipant.create(user = "neillz", event = testingEvent)
        EventParticipant.create(user = "khatts", event = testingEvent)
        EventParticipant.create(user = "ayisie", event = testingEvent)
        

        EventRsvp.create(event=testingEvent, user="partont")

        # get event participants for the event
        eventNonAttendedData, eventWaitlistData, eventVolunteerData, eventParticipants = sortParticipantsByStatus(testingEvent)
        assert eventNonAttendedData == ["partont"]
        assert eventWaitlistData == []
        assert eventVolunteerData == ["neillz", "khatts", "ayisie"]

        # test a past event
         # add the test data
            # create an event 
            # add the event participants(attended)
            # add the rsvped
            
        # verify if the wailist is empty
        # verify if the list of participants is correct
        # verify if those who rsvped and did not attend are in non-attended list 

    

        # test a upcoming event

            # add our test data
                # create an event
                # add rsvpd users
                # add users to waitlist

            # verify that non attended is empty
            # verify that the other lists are sorted properly

        transaction.rollback()

  
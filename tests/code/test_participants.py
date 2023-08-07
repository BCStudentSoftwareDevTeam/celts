from pprint import isrecursive
import pytest
from datetime import datetime, timedelta
from peewee import IntegrityError, DoesNotExist
from app import app
from flask import g
from werkzeug.datastructures import ImmutableMultiDict

from app.models import mainDB
from app.models.user import User
from app.models.event import Event
from app.models.term import Term
from app.models.program import Program
from app.models.eventParticipant import EventParticipant
from app.logic.volunteers import getEventLengthInHours, updateEventParticipants
from app.logic.participants import unattendedRequiredEvents, addBnumberAsParticipant, getEventParticipants, trainedParticipants, getParticipationStatusForTrainings, checkUserRsvp, checkUserVolunteer, addPersonToEvent
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
def test_checkUserRsvp():
    with mainDB.atomic() as transaction:
        newEvent = Event.create(term = 2, program = 9)
        user = User.get_by_id("ramsayb2")

        rsvpExists = checkUserRsvp(user, newEvent)
        assert rsvpExists == False

        EventRsvp.create(event=newEvent, user=user)
        rsvpExists = checkUserRsvp(user, newEvent)
        assert rsvpExists == True

        transaction.rollback()

@pytest.mark.integration
def test_checkUserVolunteer():
    with mainDB.atomic() as transaction:
        newEvent = Event.create(term = 2, program = 9)
        user = User.get_by_id("ramsayb2")

        rsvpExists = checkUserRsvp(user, newEvent)
        assert rsvpExists == False

        EventRsvp.create(event=newEvent, user=user)
        rsvpExists = checkUserRsvp(user, newEvent)
        assert rsvpExists == True

        transaction.rollback()

@pytest.mark.integration
def test_addPersonToEvent():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            yesterday = datetime.today() - timedelta(days=1)
            newEvent = Event.create(name = "Test event 1234", term = 2,
                                    startDate=yesterday.date(),
                                    endDate=yesterday.date(),
                                    isRsvpRequired = True,
                                    program = 9)
            
            newEvent = Event.get(name="Test event 1234")

            user = User.get_by_id("ramsayb2")
            userAdded = addPersonToEvent(user, newEvent)
            assert userAdded == True, "User was not added"
            assert checkUserVolunteer(user, newEvent), "No Volunteer record was added"
            assert not checkUserRsvp(user, newEvent), "An RSVP record was added instead"
            transaction.rollback()

            tomorrow = datetime.today() + timedelta(days=1)
            newEvent = Event.create(name = "Test event 1234", 
                                    term = 2,
                                    startDate=tomorrow.date(),
                                    endDate=tomorrow.date(),
                                    isRsvpRequired = True,
                                    program = 9)
            
            newEvent = Event.get(name="Test event 1234")

            userAdded = addPersonToEvent(user, newEvent)
            assert userAdded == True, "User was not added"
            assert checkUserRsvp(user, newEvent), "No RSVP record was added"
            assert not checkUserVolunteer(user, newEvent), "A Volunteer record was added instead"
            transaction.rollback()

            tomorrow = datetime.today() + timedelta(days=1)
            testWaitlistEvent = Event.create(name = "Waitlist Event",
                                            term = 2,
                                            startDate = tomorrow.date(),
                                            endDate = tomorrow.date(),
                                            isRsvpRequired = True,
                                            rsvpLimit = 1,
                                            program = 9)
            waitlistEvent = Event.get(name="Waitlist Event")
            rsvpUser = User.get_by_id("ayisie")
            
            addRsvp = addPersonToEvent(rsvpUser, waitlistEvent)
            rsvpNoWaitlist = list(EventRsvp.select().where(EventRsvp.event_id == testWaitlistEvent.id, EventRsvp.rsvpWaitlist == False))
            assert addRsvp == True
            assert len(rsvpNoWaitlist) == 1

            waitlistUser = User.get_by_id("partont")
            addWaitlist = addPersonToEvent(waitlistUser, waitlistEvent)
            rsvpWaitlist = EventRsvp.select().where(EventRsvp.event_id == testWaitlistEvent.id, EventRsvp.rsvpWaitlist == True)
            
            assert addWaitlist == True
            assert len(rsvpWaitlist) == 1
            assert len(rsvpNoWaitlist) == 1
        
        transaction.rollback()

@pytest.mark.integration
def test_updateEventParticipants():
    # tests if the volunteer table gets succesfully updated
    participantData = ImmutableMultiDict({'inputHours_agliullovak':100, 'checkbox_agliullovak':"on", 'event':3, 'username': 'agliullovak'})
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    # tests if user does not exist in the database
    participantData = ImmutableMultiDict({'inputHours_jarjug':100, 'checkbox_jarjug':"on", 'event':3, 'username': 'jarjug'})
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == False

    # tests for the case when the checkbox is not checked (user is not present)
    participantData = ImmutableMultiDict({'inputHours_agliullovak':100, 'event':3, 'username': 'agliullovak'})
    volunteerTableUpdate = updateEventParticipants(participantData)
    assert volunteerTableUpdate == True

    #Undo the above test changes
    participantData = ImmutableMultiDict({'inputHours_agliullovak':2, 'checkbox_agliullovak':"on", 'event':3, 'username': 'agliullovak'})

@pytest.mark.integration
def test_trainedParticipants():
    currentTerm = Term.get(Term.isCurrentTerm==1)
    with mainDB.atomic() as transaction:
        bloo = Event.create(name = "Hunger Initiatives test event",
                            term = currentTerm,
                            description= "This Event is created to do whatever.",
                            timeStart= "06:00 PM",
                            timeEnd= "09:00 PM",
                            location = "Your Father's House",
                            isRsvpRequired = 0,
                            isTraining = 1,
                            isService = 0,
                            startDate= "2021-12-12",
                            recurringId = None,
                            program = Program.get_by_id(1))
        
        #User object to be compared in assert statements
        khatts = User.get_by_id('khatts')
        neillz = User.get_by_id('neillz')
        ayisie = User.get_by_id('ayisie')
        EventParticipant.create(user="neillz", event=Event.get_by_id(14))
        EventParticipant.create(user="khatts", event=Event.get_by_id(14))
        EventParticipant.create(user="ayisie", event=Event.get_by_id(14))

        # Case1: test for an event All Volunteer Training is still checked from the first term in the 3rd term of the academic year.
        attendedPreq = trainedParticipants(3, currentTerm)
        assert khatts in attendedPreq

        # Case2: test for a different program that has a training created for it.
        attendedPreq = trainedParticipants(1, currentTerm)
        assert attendedPreq == []
        
        # Case3: test that 'khatts' is in attendedPreq after being added as a participant to the training.  
        EventParticipant.create(user = khatts, event=Event.get_by_id(bloo))
        attendedPreq = trainedParticipants(1, currentTerm)
        assert attendedPreq == [khatts]

        # Case4: test for when user changes current term but is still in the same academic year and we have some more people. 
        currentTerm = Term.get_by_id(2)
        attendedPreq = trainedParticipants(1, currentTerm)
        assert attendedPreq == [neillz, khatts, ayisie]

        transaction.rollback()

    with mainDB.atomic() as transaction:
        Event.update(program = 3).where(Event.id== 14).execute() # require AVT
        
        attendedPreq = trainedParticipants(3, currentTerm)
        assert attendedPreq == []   # no user has completed both AVT and ACT for program 3

        EventParticipant.create(user="khatts", event=14)
        attendedPreq = trainedParticipants(3, currentTerm)
        assert attendedPreq == [khatts]   # "khatts" has completed both AVT and ACT for program 3

        transaction.rollback()

    # Neither AVT nor ACT is required
    currentTerm = Term.get_by_id(6)
    attendedPreq = trainedParticipants(4, currentTerm)
    assert attendedPreq == []


# tests for unattendedRequiredEvents
@pytest.mark.integration
def test_unattendedRequiredEvents():

    # test unattended events
    program = 1
    user = 'ramsayb2'

    unattendedEvents = unattendedRequiredEvents(program, user)
    assert len(unattendedEvents) == 1

    # test after user has attended an event
    with mainDB.atomic() as transaction:
        event = Event.get(Event.name == unattendedEvents[0])
        EventParticipant.create(user = user, event = event)

        unattendedEvents = unattendedRequiredEvents(program, user)
        assert len(unattendedEvents) == 0

        mainDB.rollback()

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
    assert unattendedEvents == ['Empty Bowls Spring Event 1']

@pytest.mark.integration
def test_addBnumberAsParticipant():
    # Tests the Kiosk
    # user is banned
    with mainDB.atomic() as transaction:
        signedInUser, userStatus = addBnumberAsParticipant("B00739736", 2)
        assert userStatus == "banned"


        # user is already signed in
        signedInUser, userStatus = addBnumberAsParticipant("B00751360", 2)
        assert userStatus == "already signed in"

        # user is eligible but the user is not in EventParticipant and EventRsvp
        signedInUser = User.get(User.bnumber=="B00759117")
        with pytest.raises(DoesNotExist):
            EventParticipant.get(EventParticipant.user==signedInUser, EventParticipant.event==2)
            EventRsvp.get(EventRsvp.user==signedInUser, EventRsvp.event==2)

            signedInUser, userStatus = addBnumberAsParticipant("B00759117", 2)
            assert userStatus == "success"

            participant = EventParticipant.select().where(EventParticipant.event==2, EventParticipant.user==signedInUser)
            assert "agliullovak" in participant

            userRsvp = EventRsvp.select().where(EventRsvp.event==2, EventRsvp.user==signedInUser)
            assert "agliullovak" in userRsvp

            EventParticipant.delete(EventParticipant.user==signedInUser, EventParticipant.event==2).execute()
            EventRsvp.delete(EventRsvp.user==signedInUser, EventRsvp.event==2).execute()
        mainDB.rollback()

@pytest.mark.integration
def test_getEventParticipants():
    event = Event.get_by_id(1)

    khatts = User.get_by_id('khatts')

    eventParticipantsDict = getEventParticipants(event)
    assert khatts in eventParticipantsDict
    assert eventParticipantsDict[khatts] == 2

@pytest.mark.integration
def test_getEventParticipantsWithWrongParticipant():
    event = Event.get_by_id(1)
    eventParticipantsDict = getEventParticipants(event)
    assert "agliullovak" not in eventParticipantsDict

@pytest.mark.integration
def test_getParticipationStatusForTrainings():
    with mainDB.atomic() as transaction:
        currentTerm = Term.get_by_id(3)
        academicYear = currentTerm.academicYear

        testingEvent = Event.create(name = "Testing delete event",
                                    term = 2,
                                    description= "This Event is Created to be Deleted.",
                                    timeStart= "06:00 PM",
                                    timeEnd= "09:00 PM",
                                    location = "Your Father's House",
                                    isRsvpRequired = 0,
                                    isTraining = 1,
                                    isService = 0,
                                    startDate= "2021-12-12",
                                    recurringId = None,
                                    program = Program.get_by_id(8))

        allProgramTrainings = (Event.select().join(Term)
                                    .where(Event.isTraining == True,
                                          (Event.program == Program.get_by_id(2)) | 
                                          (Event.isAllVolunteerTraining == True),
                                           Event.term.academicYear == academicYear)
                              )
        listOfProgramTrainings = [programTraining for programTraining in allProgramTrainings]
        for training in listOfProgramTrainings:
            assert training.term.academicYear == currentTerm.academicYear

        # If the user has participated in every training, assert their participated status for that training == 1
        for training in listOfProgramTrainings:
            EventParticipant.create(user = User.get_by_id("ramsayb2"), event = training)
        programTrainings = getParticipationStatusForTrainings(Program.get_by_id(2), [User.get_by_id("ramsayb2")], currentTerm)
        for program, attended in programTrainings['ramsayb2']:
            assert attended == 1
        transaction.rollback()

        # If the user "attended" the training, assert their participated status == 1, otherwise, assert participated status == 0
        # only make the user a participant on even iterations
        for counter, training in enumerate(listOfProgramTrainings):
            if (counter % 2) == 0:
                EventParticipant.create(user = User.get_by_id("ramsayb2"), event = training)

        programTrainings = getParticipationStatusForTrainings(Program.get_by_id(2), [User.get_by_id("ramsayb2")], currentTerm)
        for counter, (training, attended) in enumerate(programTrainings['ramsayb2']):
            if (counter % 2) == 0:
                assert attended == 1
            else:
                assert attended == 0
        transaction.rollback()

        # If the user has not participated in any trainings, assert their participated status for that training == 1
        programTrainings = getParticipationStatusForTrainings(Program.get_by_id(2), [User.get_by_id("ramsayb2")], currentTerm)
        for training, attended in programTrainings['ramsayb2']:
            assert attended == 0
        transaction.rollback()

        futureYear = 2030
        futureTerm = Term.create(description = 'A test term in the future',
                                 year = 2030,
                                 academicYear = f"{futureYear}-{futureYear+1}",
                                 isSummer = False,
                                 isCurrentTerm = False,
                                 termOrder = f"{futureYear}-1")
        testingEvent = Event.create(name = "Testing delete event",
                                    term = futureTerm,
                                    description= "This Event is Created to be Deleted.",
                                    timeStart= "06:00 PM",
                                    timeEnd= "09:00 PM",
                                    location = "Your Mother's House",
                                    isRsvpRequired = 0,
                                    isTraining = 1,
                                    isService = 0,
                                    startDate= f"{futureYear}-12-12",
                                    recurringId = None,
                                    program = Program.get_by_id(8))

          
        # If the event has not occurred yet, assert that someone who has rsvp'd is true and someone who hasn't is false
        EventRsvp.create(user = User.get_by_id("ramsayb2"), event = testingEvent)
        programTrainings = getParticipationStatusForTrainings(Program.get_by_id(8), [User.get_by_id('ramsayb2'), User.get_by_id('neillz')], futureTerm)
        for training, attended in programTrainings['ramsayb2']:
            assert attended == 1
        for training, attended in programTrainings['neillz']:
            assert attended == 0
        transaction.rollback()

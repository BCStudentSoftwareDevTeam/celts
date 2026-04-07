import pytest
import datetime
from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant

from app.logic.volunteerSpreadsheet import *

@pytest.fixture
def fixture_info():
    with mainDB.atomic() as transaction:
        user1 = User.create(username="doej", firstName="John", lastName="Doe", bnumber="B774377", major="Graphics Design", rawClassLevel="Sophomore")
        user2 = User.create(username="doej2", firstName="Jane", lastName="Doe", bnumber="B888828", major="Biology", rawClassLevel="Junior")
        user3 = User.create(username="builderb", firstName="Bob", lastName="Builder", bnumber="B00700932", major="Construction", rawClassLevel="Senior")

        term1 = Term.create(id=500, description='Fall 2023', academicYear='2023-2024')
        term2 = Term.create(id=600, description='Fall 2024', academicYear='2024-2025')
        term3 = Term.create(id=700, description='Spring 2024', academicYear='2023-2024')
        term4 = Term.create(id=800, description='Spring 2025', academicYear='2024-2025')

        program1 = Program.create(id=501, programName='Program1')
        program2 = Program.create(id=502, programName='Program2')
        program3 = Program.create(id=503, programName='Program3')
        program4 = Program.create(id=504, programName='Program4')

        event1 = Event.create(id=501, name='Event1', term=term1, program=program1)
        event2 = Event.create(id=502, name='Event2', term=term1, program=program2)
        event3 = Event.create(id=503, name='Event3', term=term1, program=program3)
        event4 = Event.create(id=504, name='Event4', term=term2, program=program4)

        eventparticipant1 = EventParticipant.create(event=event1, user=user1, hoursEarned=5)
        eventparticipant2 = EventParticipant.create(event=event1, user=user2, hoursEarned=3)
        eventparticipant4 = EventParticipant.create(event=event4, user=user3, hoursEarned=0)

        yield {
            'user1': user1,
            'user2': user2,
            'user3': user3,
            'term1': term1,
            'term2': term2,
            'program1': program1,
            'program2': program2,
            'program3': program3,
            'program3': program3,
            'event1': event1,
            'event2': event2,
            'event3': event3,
            'event4': event4,
            'eventparticipant1': eventparticipant1,
            'eventparticipant2': eventparticipant2,
            'eventparticipant4': eventparticipant4,
        }

        transaction.rollback()


def test_createSpreadsheet(fixture_info):
    fixtureData = fixture_info
    createSpreadsheet("2023-2024")
    createSpreadsheet("2024-2025")

def test_calculateRetentionRate():
    # Takes 2 dictionaries, a fall and spring dictionary and see who has returned in the spring from the fall term
    fallDict = ({'Adopt-a-Grandparent': ['curiem'], 'CELTS-Sponsored Event': [None]})
    springDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'doej2']})
    assert calculateRetentionRate(fallDict, springDict) == {'Adopt-a-Grandparent': 0.0, 'CELTS-Sponsored Event': 0.0}

    fallDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'doej2']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 1.0}

    springDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'ayisie']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 0.75}

def test_removeNullParticipants():
    #Removes empty elements fromm a list
    testInputList = ['khatts']
    assert removeNullParticipants(testInputList) == ['khatts']
    testInputList = ['khatts', '', 'ayisie']
    assert removeNullParticipants(testInputList) == ['khatts', 'ayisie']

def test_termParticipation(fixture_info):
    # Checks who all participated in any given program for an even. NONE will be the result if there was an event for a program without and participants.
    assert termParticipation(fixture_info['term1']) == {'Program1': ['doej', 'doej2'], 
                                                        'Program2': [None], 'Program3': [None] }
    assert termParticipation(fixture_info['term2']) == {'Program4': ['builderb']}

    EventParticipant.create(user = 'builderb',
                            event = fixture_info['event1'],
                            hoursEarned = 1)
    termParticipationResult = termParticipation('Fall 2023')
    for participantList in termParticipationResult.values():
        participantList.sort()
    assert termParticipationResult == {'Program1': ['builderb', 'doej', 'doej2'], 'Program2': [None], 'Program3': [None]}

    EventParticipant.create(user = 'builderb',
                            event = fixture_info['event2'],
                            hoursEarned = 1)
    termParticipationResult = termParticipation('Fall 2023')
    for participantList in termParticipationResult.values():
        participantList.sort()
    assert termParticipationResult == {'Program1': ['builderb', 'doej', 'doej2'], 'Program2': ['builderb'], 'Program3': [None]}

def test_getRetentionRate(fixture_info):
    #Takes an academic year and returns how many people were retained across terms by percentage for each program.
    assert sorted(getRetentionRate("2023-2024")) == [('Program1', '0.0%'), 
                                                        ('Program2', '0.0%'),
                                                        ('Program3', '0.0%')]
    assert sorted(getRetentionRate("2024-2025")) == [('Program4', '0.0%')]

    testTerm = Term.create(id=501, description='Spring 2024', academicYear='2023-2024')
    springEvent = Event.create(name = "Spring2021Event", 
                                program=  fixture_info['program1'], 
                                term = testTerm)
    
    EventParticipant.create(user='doej',
                            event=springEvent,
                            hoursEarned=1)
    
    # Check for john doe participating in both semesters
    assert sorted(getRetentionRate("2023-2024")) == [('Program1', '50.0%'), 
                                                        ('Program2', '0.0%'),
                                                        ('Program3', '0.0%')]
    
    EventParticipant.create(user='doej2',
                            event=springEvent,
                            hoursEarned=1)
    
    # Checks for all previous participants in both semesters  
    assert sorted(getRetentionRate("2023-2024")) == [('Program1', '100.0%'), 
                                                        ('Program2', '0.0%'),
                                                        ('Program3', '0.0%')]

def test_repeatVolunteers(fixture_info):
    #repeat volunteers people who participated in more than one event
    testEvent = Event.create(name="Test Event",
                                term=fixture_info["term1"],
                                program=fixture_info['program1'])
    EventParticipant.create(user='doej',
                            event=testEvent,
                            hoursEarned=1)
    
    assert sorted(list(repeatVolunteers("2023-2024"))) == [('John Doe', 2)]
    assert list(repeatVolunteers("2024-2025")) == []

    testEvent2 = Event.create(name="Spring2021Event",
                                term=fixture_info["term1"],
                                program=fixture_info['program1'])
    
    EventParticipant.create(user = 'doej', event = testEvent2, hoursEarned=0)
    
    # Check for separate events
    assert sorted(list(repeatVolunteers("2023-2024"))) == [('John Doe', 3)]

    testEvent2 = Event.create(name="Spring2021Event",
                                term=fixture_info["term1"],
                                program=fixture_info['program2'])
    EventParticipant.create(user='doej', 
                            event=testEvent2,
                            hoursEarned=1)
    
    # Check for event from a seprate events and programs
    assert sorted(list(repeatVolunteers("2023-2024"))) == [('John Doe', 4)]

def test_repeatVolunteersPerProgram(fixture_info):
    # Find people who have participated in two events of the same program
    assert sorted(list(repeatVolunteersPerProgram("2023-2024"))) == [] 
    
    testEvent3 = Event.create(name="Test Event",
                                term=fixture_info['term1'], 
                                program=fixture_info['program1'])
    EventParticipant.create(user='doej',
                            event=testEvent3,
                            hoursEarned=1)
    
    assert sorted(list(repeatVolunteersPerProgram("2023-2024"))) == [('John Doe', 'Program1', 2)] 
    assert sorted(list(repeatVolunteersPerProgram("2024-2025"))) == [] 

    testEvent4 = Event.create(name="Test Event 2",
                                term=fixture_info['term1'], 
                                program=fixture_info['program1'])
    EventParticipant2 = EventParticipant.create(user='doej',
                                                event=testEvent4,
                                                hoursEarned=1)
    
    assert sorted(list(repeatVolunteersPerProgram("2023-2024"))) == [('John Doe', 'Program1', 3)]

def test_volunteerMajorAndClass(fixture_info): 
    # Gets the list of majors or the class levels of volunteers
    assert list(volunteerMajorAndClass("2023-2024", User.major)) == list([('Biology', 1), ('Graphics Design', 1)])
    assert list(volunteerMajorAndClass("2023-2024", User.rawClassLevel)) == [('Junior', 1), ('Sophomore', 1)]
    assert list(volunteerMajorAndClass("2023-2024", User.rawClassLevel, True)) == [('Sophomore', 1), ('Junior', 1)]

    assert list(volunteerMajorAndClass("2024-2025", User.major)) == list([('Construction', 1)])
    assert list(volunteerMajorAndClass("2024-2025", User.rawClassLevel)) == [('Senior', 1)]
    assert list(volunteerMajorAndClass("2024-2025", User.rawClassLevel, True)) == [('Senior', 1)]

    User.create(username = 'solijonovam',
                email = 'solijonovam@berea.edu',
                firstName = 'Madinabonu',
                lastName  = 'Solijonova',
                major = 'Agriculture',
                rawClassLevel = 'Sophomore')
    EventParticipant.create(user = 'solijonovam',
                            event = fixture_info['event1'],
                            hoursEarned = 2)
    EventParticipant.create(event=fixture_info['event1'],
                            user=fixture_info['user3'],
                            hoursEarned=3)

    # Checks for event participants changes 
    assert list(volunteerMajorAndClass("2023-2024", User.major)) == [('Agriculture', 1), ('Biology', 1), ('Construction', 1), ('Graphics Design', 1)]
    assert list(volunteerMajorAndClass("2023-2024", User.rawClassLevel)) == [('Junior', 1), ('Senior', 1), ('Sophomore', 2)]
    assert list(volunteerMajorAndClass("2023-2024", User.rawClassLevel, True)) == [('Sophomore', 2), ('Junior', 1), ('Senior', 1)]

def test_volunteerHoursByProgram(fixture_info):
    # Gets the list of volunteer hours per program as a tuple
    assert list(volunteerHoursByProgram("2023-2024")) == [('Program1', 8.0)]
    assert list(volunteerHoursByProgram("2024-2025")) == [('Program4', 0.0)]
    
    EventParticipant.create(event=fixture_info["event1"], 
                            user=fixture_info["user3"], 
                            hoursEarned=10)

    # Check for newly added participant
    assert list(volunteerHoursByProgram("2023-2024")) == [('Program1', 18.0)]

def test_onlyCompletedAllVolunteer(fixture_info): 
    # This function returns a list of usernames and fullnames for people who have only completed all volunteer training in a particular academic year.
    assert list(onlyCompletedAllVolunteer("2023-2024")) == []

    allVolunteerEvent = Event.create(name="All Volunteer Training",
                                term=fixture_info['term1'],
                                program=fixture_info['program1'],
                                isTraining=1,
                                isAllVolunteerTraining=1)
    EventParticipant.create(user = 'builderb', # Not participated in event
                            event = allVolunteerEvent, # Added to all volunteer training event
                            hoursEarned = 1)

    assert list(onlyCompletedAllVolunteer("2023-2024")) == [('builderb', 'Bob Builder')]
    assert list(onlyCompletedAllVolunteer("2024-2025")) == []

    testEvent = Event.create(name="Test Event",
                                program=fixture_info['program1'],
                                term=fixture_info['term1'])
    EventParticipant.create(user = 'builderb', # Only participated in all volunteer event
                            event = testEvent,
                            hoursEarned = 1)

    # Checks whether participant is removed from the list 
    assert list(onlyCompletedAllVolunteer("2023-2024")) == []

def test_volunteerProgramHours(fixture_info):
    # Returns list of (program, username, hours) for each program
    assert sorted(list(volunteerProgramHours("2023-2024"))) == [('Program1', 'doej', 5.0), ('Program1', 'doej2', 3.0)]
    assert sorted(list(volunteerProgramHours("2024-2025"))) == [('Program4', 'builderb', 0.0)]

    EventParticipant.create(user = 'doej',
                            event = fixture_info['event2'],
                            hoursEarned = 1)
    
    # Test for changes between fixture and new event 
    assert sorted(list(volunteerProgramHours("2023-2024"))) == [('Program1', 'doej', 5.0), ('Program1', 'doej2', 3.0), ('Program2', 'doej', 1.0)]
    
    testEvent = Event.create(name="Test Event",
                                program=fixture_info['program1'],
                                term=fixture_info['term1'])
    EventParticipant.create(user = 'doej',
                            event = testEvent,
                            hoursEarned = 2)
    
    # Test with additional event creation
    assert sorted(list(volunteerProgramHours("2023-2024"))) == [('Program1', 'doej', 7.0), ('Program1', 'doej2', 3.0), ('Program2', 'doej', 1.0)]

def test_totalVolunteerHours(fixture_info):
    #Returns the total amount of volunteer hours in the database
    assert list(totalVolunteerHours("2023-2024")) == [(8.0,)]
    assert list(totalVolunteerHours("2024-2025")) == [(0.0,)]

    #hoursEarned is set to 0 (none)
    EventParticipant.create(user = 'builderb',
                            event = fixture_info['event3'],
                            hoursEarned = 0)
    assert list(totalVolunteerHours("2023-2024")) == [(8.0,)] 
    assert list(totalVolunteerHours("2024-2025")) == [(0.0,)] #tests for hoursEarned to be 0 (should pass)
    #assert list(totalVolunteerHours("2024-2025")) == [(None,)] #tests for hoursEarned to be None (should fail)

        
    # Adding 1 volunteer hour to one event
    EventParticipant.create(user = 'builderb',
                            event = fixture_info['event2'],
                            hoursEarned = 1)
    
    # Checking that the total volunteer hours has increased by 1
    assert list(totalVolunteerHours("2023-2024")) == [(9.0,)]
    EventParticipant.create(user = 'doej',
                            event = fixture_info['event1'],
                            hoursEarned = 3)
    
    # Checking increase by multiple hours
    assert list(totalVolunteerHours("2023-2024")) == [(12.0,)]

def test_getVolunteerProgramEventByTerm(fixture_info):
# Returns a list for every eventparticipant entry for (full name, username, program, and event) for a given term
    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(fixture_info['term1']))) == ([('John Doe', 'doej', 'Program1', 'Event1'), 
                                                                                            ('Jane Doe', 'doej2', 'Program1', 'Event1')])
    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(fixture_info['term2']))) == ([('Bob Builder', 'builderb', 'Program4', 'Event4')])
    

    EventParticipant.create(user = 'builderb', event = fixture_info['event2'], hoursEarned=0)
    
    # Checks for additional volunteer participants
    assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(fixture_info['term1'])))) == [('Bob Builder', 'builderb', 'Program2', 'Event2'),
                                                                                                    ('Jane Doe', 'doej2', 'Program1', 'Event1'),
                                                                                                    ('John Doe', 'doej', 'Program1', 'Event1')]
    
    testEvent = Event.create(name="Test Event",
                                term= fixture_info['term1'],
                                program = fixture_info['program2'])
    testEvent2 = Event.create(name = "Test Event 2",
                                term = fixture_info['term1'],
                                program=fixture_info['program2'])
    EventParticipant.create(user='doej',
                            event=testEvent, hoursEarned=0)
    EventParticipant.create(user='doej',
                            event=testEvent2, hoursEarned=0)
    
    # Checks for repeated volunteers 
    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(fixture_info['term1']))) == [('Bob Builder', 'builderb', 'Program2', 'Event2'),
                                                                                            ('John Doe', 'doej', 'Program1', 'Event1'),
                                                                                            ('John Doe', 'doej', 'Program2', 'Test Event'),
                                                                                            ('John Doe', 'doej', 'Program2', 'Test Event 2'),
                                                                                            ('Jane Doe', 'doej2', 'Program1', 'Event1')]
    
    assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(fixture_info['term1'])))) == [('Bob Builder', 'builderb', 'Program2', 'Event2'),
                                                                                                    ('Jane Doe', 'doej2', 'Program1', 'Event1'),
                                                                                                    ('John Doe', 'doej', 'Program1', 'Event1'),
                                                                                                    ('John Doe', 'doej', 'Program2', 'Test Event'),
                                                                                                    ('John Doe', 'doej', 'Program2', 'Test Event 2')]

def test_getUniqueVolunteers(fixture_info):
    # Returns a list of everyone who has volunteered.
    assert sorted(list(getUniqueVolunteers("2023-2024"))) == [('doej', 'John Doe', 'B774377'),
                                                                ('doej2', 'Jane Doe', 'B888828'),]
    assert list(getUniqueVolunteers("2024-2025")) == [('builderb', 'Bob Builder', 'B00700932')]
    
    EventParticipant.create(user = 'builderb', event = fixture_info['event1'], hoursEarned=0)
    
    # Checks for new event participants
    assert sorted(list(getUniqueVolunteers("2023-2024"))) == [('builderb', 'Bob Builder', 'B00700932'),
                                                                ('doej', 'John Doe', 'B774377'),
                                                                ('doej2', 'Jane Doe', 'B888828')]
    
    User.create(username="testt", firstName="Test", lastName="Tester", bnumber="B55555")
    testEvent = Event.create(name="Test Event",
                                term = fixture_info['term1'],
                                program = fixture_info['program1'])
    EventParticipant.create(user = 'testt',    
                            event = testEvent,
                            hoursEarned = 1)
    
    # Check for additional user
    assert sorted(list(getUniqueVolunteers("2023-2024"))) == [('builderb', 'Bob Builder', 'B00700932'),
                                                                ('doej', 'John Doe', 'B774377'),
                                                                ('doej2', 'Jane Doe', 'B888828'),
                                                                ('testt', 'Test Tester', 'B55555')]

@pytest.mark.integration
def test_graduatingSeniorsVolunteerHours(fixture_info):
    columns, rows = graduatingSeniorsVolunteerHours("2024-2025-test")
    assert columns == ["Full Name", "Email", "B-Number", "Unique Volunteer Semesters", "Total Volunteer Hours"]

    assert list(rows) == []

    term5 = Term.create(description='Fall 2021', academicYear='2021-2022-test')
    term6 = Term.create(description='Spring 2022', academicYear='2021-2022-test')
    term7 = Term.create(description='Fall 2022', academicYear='2022-2023-test')

    program5 = Program.create(programName='Program5')

    event5 = Event.create(name='Event5', term=term5, program=program5, startDate=date(2021, 9, 1),
                          isCanceled=False, deletionDate=None, isService=True)
    event6 = Event.create(name='Event6', term=term6, program=program5, startDate=date(2022, 2, 1),
                          isCanceled=False, deletionDate=None, isService=True)
    event7 = Event.create(name='Event7', term=term7, program=program5, startDate=date(2022, 9, 1),
                          isCanceled=False, deletionDate=None, isService=True)

    # Give Bob 3 more unique semesters of service (he already has 1 from before - term2/2024-2025)
    EventParticipant.create(user=fixture_info['user3'], event=event5, hoursEarned=2)
    EventParticipant.create(user=fixture_info['user3'], event=event6, hoursEarned=3)
    EventParticipant.create(user=fixture_info['user3'], event=event7, hoursEarned=4)

    # Bob now has 4 unique semesters total, and is a Senior in 2024-2025-test, so his info should appear
    columns, rows = graduatingSeniorsVolunteerHours("2024-2025-test")
    result = list(rows)
    assert len(result) == 1
    assert result[0] == ("Bob Builder", "builderb@berea.edu", "B00700932", 4, 9.0)

    # Bob should NOT appear when querying a year where he is not a Senior (Bob is Senior only in 2024-2025)
    columns, rows = graduatingSeniorsVolunteerHours("2023-2024-test")
    assert list(rows) == []

    # non-senior students should never appear even with enough semesters
    extraTerm = Term.create(description='Spring 2021', academicYear='2020-2021-test')
    extraTerm2 = Term.create(description='Fall 2020', academicYear='2020-2021-test')
    extraTerm3 = Term.create(description='Spring 2020', academicYear='2019-2020-test')

    event8 = Event.create(name='Event8', term=extraTerm, program=program5, startDate=date(2021, 2, 1),
                          isCanceled=False, deletionDate=None, isService=True)
    event9 = Event.create(name='Event9', term=extraTerm2, program=program5, startDate=date(2020, 9, 1),
                          isCanceled=False, deletionDate=None, isService=True)
    event10 = Event.create(name='Event10', term=extraTerm3, program=program5, startDate=date(2020, 2, 1),
                           isCanceled=False, deletionDate=None, isService=True)

    # give John (Sophomore) 4 unique semesters, so it should never appear
    EventParticipant.create(user=fixture_info['user1'], event=event8, hoursEarned=1)
    EventParticipant.create(user=fixture_info['user1'], event=event9, hoursEarned=1)
    EventParticipant.create(user=fixture_info['user1'], event=event10, hoursEarned=1)
    # John already has term1 (2023-2024-test) from fixture, so now has 4 unique semesters
    columns, rows = graduatingSeniorsVolunteerHours("2023-2024-test")
    assert list(rows) == []

    # Test "Graduating" class level works the same as "Senior"
    graduatingUser = User.create(username="smithj", firstName="James", lastName="Smith",
                                 bnumber="B999999", major="Math", rawClassLevel="Graduating")

    gradTerm1 = Term.create(description='Fall 2023 Grad', academicYear='2023-2024-test')
    gradTerm2 = Term.create(description='Spring 2023 Grad', academicYear='2022-2023-test')
    gradTerm3 = Term.create(description='Fall 2022 Grad', academicYear='2022-2023-test')
    gradTerm4 = Term.create(description='Spring 2022 Grad', academicYear='2021-2022-test')

    gevent1 = Event.create(name='GEvent1', term=gradTerm1, program=program5, startDate=date(2023, 9, 5),
                           isCanceled=False, deletionDate=None, isService=True)
    gevent2 = Event.create(name='GEvent2', term=gradTerm2, program=program5, startDate=date(2023, 2, 5),
                           isCanceled=False, deletionDate=None, isService=True)
    gevent3 = Event.create(name='GEvent3', term=gradTerm3, program=program5, startDate=date(2022, 9, 5),
                           isCanceled=False, deletionDate=None, isService=True)
    gevent4 = Event.create(name='GEvent4', term=gradTerm4, program=program5, startDate=date(2022, 2, 5),
                           isCanceled=False, deletionDate=None, isService=True)

    EventParticipant.create(user=graduatingUser, event=gevent1, hoursEarned=5)
    EventParticipant.create(user=graduatingUser, event=gevent2, hoursEarned=5)
    EventParticipant.create(user=graduatingUser, event=gevent3, hoursEarned=5)
    EventParticipant.create(user=graduatingUser, event=gevent4, hoursEarned=5)

    columns, rows = graduatingSeniorsVolunteerHours("2023-2024-test")
    result = list(rows)
    assert len(result) == 1
    assert result[0] == ("James Smith", "smithj@berea.edu", "B999999", 4, 20.0)

    # non-service events should not be counted
    nonServiceTerm = Term.create(description='Fall 2019', academicYear='2019-2020-test')
    nonServiceEvent = Event.create(name='NonServiceEvent', term=nonServiceTerm, program=program5,
                                   startDate=date(2019, 9, 1), isCanceled=False, deletionDate=None, isService=False)
    EventParticipant.create(user=fixture_info['user3'], event=nonServiceEvent, hoursEarned=5)

    # Bob still has exactly 4 semesters with volunteer hours, the non-service event participation should not push the count up
    columns, rows = graduatingSeniorsVolunteerHours("2024-2025-test")
    result = list(rows)
    assert result[0][3] == 4

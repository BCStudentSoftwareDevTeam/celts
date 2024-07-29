import pytest
import datetime
from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant

from app.logic.spreadsheet import *

@pytest.fixture
def fixture_info():
    with mainDB.atomic() as transaction:
        user1 = User.create(username="doej", firstName="John", lastName="Doe", bnumber="B774377", major="Graphics Design", classLevel="Sophomore")
        user2 = User.create(username="doej2", firstName="Jane", lastName="Doe", bnumber="B888828", major="Biology", classLevel="Junior")
        user3 = User.create(username="builderb", firstName="Bob", lastName="Builder", bnumber="B00700932", major="Construction", classLevel="Senior")

        term1 = Term.create(id=500, description='Fall 2023', academicYear='2023-2024')

        program1 = Program.create(id=501, programName='Program1')
        program2 = Program.create(id=502, programName='Program2')

        event1 = Event.create(id=501, name='Event1', term=term1, program=program1)
        event2 = Event.create(id=502, name='Event2', term=term1, program=program2)

        eventparticipant1 = EventParticipant.create(event=event1, user=user1, hoursEarned=5)
        eventparticipant2 = EventParticipant.create(event=event1, user=user2, hoursEarned=3)


        yield {
            'user1': user1,
            'user2': user2,
            'user3': user3,
            'term1': term1,
            'program1': program1,
            'program2': program2,
            'event1': event1,
            'event2': event2,
            'eventparticipant1': eventparticipant1,
            'eventparticipant2': eventparticipant2,
        }

        transaction.rollback()


@pytest.mark.integration
def test_createSpreadsheet(fixture_info):
    fixtureData = fixture_info
    createSpreadsheet("2023-2024")

@pytest.mark.integration
def test_calculateRetentionRate():
    # Takes 2 dictionaries, a fall and spring dictionary and see who has returned in the spring from the fall term
    fallDict = ({'Adopt-a-Grandparent': ['curiem'], 'CELTS-Sponsored Event': [None]})
    springDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'doej2']})
    assert calculateRetentionRate(fallDict, springDict) == {'Adopt-a-Grandparent': 0.0, 'CELTS-Sponsored Event': 0.0}

    fallDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'doej2']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 1.0}

    springDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'ayisie']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 0.75}

@pytest.mark.integration
def test_removeNullParticipants():
    #Removes empty elements fromm a list
    testInputList = ['khatts']
    assert removeNullParticipants(testInputList) == ['khatts']
    testInputList = ['khatts', '', 'ayisie']
    assert removeNullParticipants(testInputList) == ['khatts', 'ayisie']

@pytest.mark.integration
def test_termParticipation(fixture_info):
    # Checks who all participated in any given program for an even. NONE will be the result if there was an event for a program without and participants.
        with mainDB.atomic() as transaction:
            assert termParticipation('Fall 2023') == {'Program1': ['doej', 'doej2'], 'Program2': [None]}

            EventParticipant.create(user = 'builderb',
                                    event = 501,
                                    hoursEarned = 1)
            termParticipationResult = termParticipation('Fall 2023')
            for participantList in termParticipationResult.values():
                participantList.sort()
            assert termParticipationResult == {'Program1': ['builderb', 'doej', 'doej2'], 'Program2': [None]}

            EventParticipant.create(user = 'builderb',
                                    event = 502,
                                    hoursEarned = 1)
            termParticipationResult = termParticipation('Fall 2023')
            for participantList in termParticipationResult.values():
                participantList.sort()
            assert termParticipationResult == {'Program1': ['builderb', 'doej', 'doej2'], 'Program2': ['builderb']}

            transaction.rollback()

@pytest.mark.integration
def test_getRetentionRate(fixture_info):
    #Takes an academic year and returns how many people were retained across terms by percentage for each program.
    with mainDB.atomic() as transaction:
        User.create(username = 'solijonovam', bnumber = 'B00769465', firstName = 'Madinabonu', lastName  = 'Solijonova', major = 'Agriculture', classLevel = 'Sophomore')
        assert sorted(getRetentionRate("2023-2024")) == [('Program1', '0.0%'), 
                                                         ('Program2', '0.0%'),]

        term2 = Term.create(id=144, description='Spring 2024', academicYear='2023-2024')

        springEvent = Event.create(name="Spring2021Event", 
                                  program= 501, # Program1 
                                  term=2)  
        EventParticipant.create(user='solijonovam',
                                event=springEvent,
                                hoursEarned=1)
        # assert sorted(getRetentionRate("2020-2021")) == [('Program1', '100.0%'), 
        #                                                  ('Program2', '0.0%')]
        transaction.rollback()

@pytest.mark.integration
def test_repeatVolunteers(fixture_info):
    #repeat volunteers people who participated in more than one event
    with mainDB.atomic() as transaction:
        EventParticipant.delete().execute()
 
        testProgram = Program.create(programName = "Test Program",
                                     programDescription = "A good program")
        testEvent = Event.create(name="Fall2020Event",
                                 term=fixture_info["term1"],
                                 program=testProgram)
        EventParticipant.create(user='doej',
                                event=testEvent,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteers(fixture_info["term1"].academicYear))) == []
        testEvent2 = Event.create(name="Spring2021Event",
                                 term=fixture_info["term1"],
                                 program=testProgram)
        EventParticipant.create(user='doej',
                                event=testEvent2,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteers(fixture_info["term1"].academicYear))) == [('John Doe', 2)]
        EventParticipant.delete().execute()
        assert sorted(list(repeatVolunteers(fixture_info["term1"].academicYear))) == []
        EventParticipant.create(user='doej',
                                event=testEvent,
                                hoursEarned=1)
        testDifferentProgram = Program.create(programName = "Test Program 2",
                                              programDescription = "A good program")
        testEvent2 = Event.create(name="Spring2021Event",
                                  term=fixture_info["term1"],
                                  program=testDifferentProgram)
        EventParticipant.create(user='doej', 
                                event=testEvent2,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteers(fixture_info["term1"].academicYear))) == [('John Doe', 2)]
        transaction.rollback()

@pytest.mark.integration
def test_repeatVolunteersPerProgram(fixture_info):
    # Find people who have participated in two events of the same program
    with mainDB.atomic() as transaction:
        # EventParticipant.delete().execute()
        user1 = fixture_info["user1"]
        program1 = fixture_info["program1"]  
        testEvent = fixture_info["event1"]
        EventParticipant2 = fixture_info["eventparticipant2"]

        assert sorted(list(repeatVolunteersPerProgram("2023-2024"))) == [] 
        
        testEvent3 = Event.create(name="Test Event",
                                 term=fixture_info['term1'], 
                                 program=fixture_info['program1'])
        EventParticipant2 = EventParticipant.create(user='doej',
                                                    event=testEvent3,
                                                    hoursEarned=1)



        assert sorted(list(repeatVolunteersPerProgram("2023-2024"))) == [('John Doe', 'Program1', 2)] 

        testEvent4 = Event.create(name="Test Event 2",
                                 term=fixture_info['term1'], 
                                 program=fixture_info['program1'])
        EventParticipant2 = EventParticipant.create(user='doej',
                                                    event=testEvent4,
                                                    hoursEarned=1)
        
        assert sorted(list(repeatVolunteersPerProgram("2023-2024"))) == [('John Doe', 'Program1', 3)]

        transaction.rollback()

@pytest.mark.integration
def test_volunteerMajorAndClass(fixture_info): 
    # Gets the list of majors or the class levels of volunteers
    with mainDB.atomic() as transaction:
        

        assert list(volunteerMajorAndClass("2023-2024", User.major)) == list([('Biology', 1), ('Graphics Design', 1)])
        assert list(volunteerMajorAndClass("2023-2024", User.classLevel)) == [('Junior', 1), ('Sophomore', 1)]
        assert list(volunteerMajorAndClass("2023-2024", User.classLevel, True)) == [('Sophomore', 1), ('Junior', 1)]

        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        EventParticipant.create(user = 'solijonovam',
                                event = fixture_info['event1'],
                                hoursEarned = 2,
                                )
        EventParticipant.create(event=fixture_info['event1'],
                                user=fixture_info['user3'],
                                hoursEarned=3)

        assert list(volunteerMajorAndClass("2023-2024", User.major)) == [('Agriculture', 1), ('Biology', 1), ('Construction', 1), ('Graphics Design', 1)]
        assert list(volunteerMajorAndClass("2023-2024", User.classLevel)) == [('Junior', 1), ('Senior', 1), ('Sophomore', 2)]
        assert list(volunteerMajorAndClass("2023-2024", User.classLevel, True)) == [('Sophomore', 2), ('Junior', 1), ('Senior', 1)]
        transaction.rollback()

@pytest.mark.integration
def test_volunteerHoursByProgram():
    # Gets the list of volunteer hours per program as a tuple
    with mainDB.atomic() as transaction:
        a = (volunteerHoursByProgram(fixture_info['term1'].academicYear))
        print("# ", a)
        assert list(volunteerHoursByProgram()) == []
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        
        assert list(volunteerHoursByProgram()) == [('Program1', 8.0)]
        transaction.rollback()

# @pytest.mark.integration
# def test_onlyCompletedAllVolunteer():
#     # This function returns a list of usernames and fullnames for people who have only completed all volunteer training in a particular academic year.
#     with mainDB.atomic() as transaction:
#         assert list(onlyCompletedAllVolunteer("2020-2021")) == []
#         User.create(username = 'solijonovam',
#                     bnumber = 'B00769465',
#                     email = 'solijonovam@berea.edu',
#                     phoneNumber = '732-384-3469',
#                     firstName = 'Madinabonu',
#                     lastName  = 'Solijonova',
#                     isStudent = True,
#                     major = 'Agriculture',
#                     classLevel = 'Sophomore')
        
#         allVolunteerEvent = Event.create(name="All Volunteer Training",
#                                  term=1,
#                                  program=9,
#                                  isTraining=1,
#                                  isAllVolunteerTraining=1)
#         EventParticipant.create(user = 'solijonovam', # Not participated in event
#                                 event = allVolunteerEvent, # Added to all volunteer training event
#                                 hoursEarned = 1)
#         assert list(onlyCompletedAllVolunteer("2020-2021")) == [('solijonovam', 'Madinabonu Solijonova')]
#         testEvent = Event.create(name="Test Event",
#                                   program=1,
#                                   term=1)
#         EventParticipant.create(user = 'solijonovam', # Only participated in all volunteer event
#                                 event = testEvent,
#                                 hoursEarned = 1)
#         assert list(onlyCompletedAllVolunteer("2020-2021")) == []
#         transaction.rollback()

# @pytest.mark.integration
# def test_volunteerProgramHours():
#     # Returns list of (program, username, hours) for each program
#     with mainDB.atomic() as transaction:
#         EventParticipant.delete().execute()
#         assert sorted(list(volunteerProgramHours())) == ([])
#         EventParticipant.create(user = 'qasema',
#                                 event = 2,
#                                 hoursEarned = 1)
#         assert sorted(list(volunteerProgramHours())) == [('Hunger Initiatives', 'qasema', 1.0)]
#         EventParticipant.create(user = 'qasema',
#                                 event = 3,
#                                 hoursEarned = 1)
#         assert sorted(list(volunteerProgramHours())) == [('Adopt-a-Grandparent', 'qasema', 1.0), ('Hunger Initiatives', 'qasema', 1.0)]
#         transaction.rollback()

# @pytest.mark.integration
# def test_totalVolunteerHours():
#     #Returns the total amount of volunteer hours in the database
#     with mainDB.atomic() as transaction:
#         EventParticipant.delete().execute()
#         Event.delete().execute()
#         Term.delete().execute()

#         Term.create(id = 1,
#                     academicYear = '2021-2022',)
        
#         assert list(totalVolunteerHours()) == [(None,)]
#         # Adding 1 volunteer hour to one event
#         Event.create(id = 2, 
#                      term_id = 1,)
#         EventParticipant.create(user = 'qasema',
#                                 event = 2,
#                                 hoursEarned = 1)
#         # Checking that the total volunteer hours has increased by 1
#         assert list(totalVolunteerHours()) == [(1.0,)]
#         EventParticipant.create(user = 'ayisie',
#                                 event = 3,
#                                 hoursEarned = 6)
#         assert list(totalVolunteerHours()) == [(7.0,)]
#         transaction.rollback()

# @pytest.mark.integration
# def test_getVolunteerProgramEventByTerm():
#     # Returns a list for every eventparticipant entry for (full name, username, program, and event) for a given term
#     with mainDB.atomic() as transaction:
#         assert list(getVolunteerProgramEventByTerm(Term.get_by_id(3))) == ([])
#         assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(2)))) == ([('Ebenezer Ayisi', 'ayisie', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
#                                                                                     ('Sreynit Khatt', 'khatts', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
#                                                                                     ('Tyler Parton', 'partont', 'Hunger Initiatives', 'Hunger Hurts'),
#                                                                                     ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
#                                                                                     ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Hunger Hurts')])

#         assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(4)))) == [('Alex Bryant', 'bryanta', 'Berea Buddies', 'Tutoring'),
#                                                                                    ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Adoption 101'),
#                                                                                    ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Meet & Greet with Grandparent')]
#         User.create(username = 'solijonovam',
#                     bnumber = 'B00769465',
#                     email = 'solijonovam@berea.edu',
#                     phoneNumber = '732-384-3469',
#                     firstName = 'Madinabonu',
#                     lastName  = 'Solijonova',
#                     isStudent = True,
#                     major = 'Agriculture',
#                     classLevel = 'Sophomore')
#         testProgram = Program.create(programName = "Test Program",
#                                      programDescription = "A good program")
#         testEvent = Event.create(name="Test Event",
#                                  term=3,
#                                  program=testProgram)
#         EventParticipant.create(user='solijonovam',
#                                 event=testEvent)
#         testEvent2 = Event.create(name="Test Event",
#                                   term=2,
#                                   program=testProgram)
#         EventParticipant.create(user='solijonovam',
#                                 event=testEvent2)
#         testEvent3 = Event.create(name="Test Event",
#                                   term=4,
#                                   program=testProgram)
#         EventParticipant.create(user='solijonovam',
#                                 event=testEvent3)
#         assert list(getVolunteerProgramEventByTerm(Term.get_by_id(3))) == [('Madinabonu Solijonova', 'solijonovam', 'Test Program', 'Test Event')]
#         assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(2)))) == [('Ebenezer Ayisi', 'ayisie', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
#                                                                                    ('Madinabonu Solijonova', 'solijonovam', 'Test Program', 'Test Event'),
#                                                                                    ('Sreynit Khatt', 'khatts', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
#                                                                                    ('Tyler Parton', 'partont', 'Hunger Initiatives', 'Hunger Hurts'), 
#                                                                                    ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
#                                                                                    ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Hunger Hurts')]

#         assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(4)))) == [('Alex Bryant', 'bryanta', 'Berea Buddies', 'Tutoring'), 
#                                                                                    ('Madinabonu Solijonova', 'solijonovam', 'Test Program', 'Test Event'),
#                                                                                    ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Adoption 101'), 
#                                                                                    ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Meet & Greet with Grandparent')]
#         transaction.rollback()

# @pytest.mark.integration
# def test_getUniqueVolunteers():
#     # Returns a list of everyone who has volunteered.
#     with mainDB.atomic() as transaction:
#         assert sorted(list(getUniqueVolunteers("2021-2022"))) == ([('bryanta', 'Alex Bryant', 'B00708826'),
#                                                                    ('khatts', 'Sreynit Khatt', 'B00759107')])
    
#         assert sorted(list(getUniqueVolunteers("2020-2021"))) == ([('ayisie', 'Ebenezer Ayisi', 'B00739736'),
#                                                                    ('khatts', 'Sreynit Khatt', 'B00759107'),
#                                                                    ('neillz', 'Zach Neill', 'B00751864'),
#                                                                    ('partont', 'Tyler Parton', 'B00751360')])
        
#         User.create(username = 'solijonovam',
#                     bnumber = 'B00769465',
#                     email = 'solijonovam@berea.edu',
#                     phoneNumber = '732-384-3469',
#                     firstName = 'Madinabonu',
#                     lastName  = 'Solijonova',
#                     isStudent = True,
#                     major = 'Agriculture',
#                     classLevel = 'Sophomore')
#         testEvent = Event.create(name="Test Event",
#                                  term=1,
#                                  program=1)
#         EventParticipant.create(user = 'solijonovam',
#                                 event = testEvent,
#                                 hoursEarned = 1)
        
#         assert sorted(list(getUniqueVolunteers("2020-2021"))) == [('ayisie', 'Ebenezer Ayisi', 'B00739736'), 
#                                                                   ('khatts', 'Sreynit Khatt', 'B00759107'), 
#                                                                   ('neillz', 'Zach Neill', 'B00751864'), 
#                                                                   ('partont', 'Tyler Parton', 'B00751360'), 
#                                                                   ('solijonovam', 'Madinabonu Solijonova', 'B00769465')]
#         transaction.rollback()



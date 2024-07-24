import pytest
import datetime

from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant

from app.logic.spreadsheet import *

@pytest.mark.integration 
@pytest.fixture
def fixture_users():
    with mainDB.atomic() as transaction:
        test_usersData = [
        {
            "username" : "ramazanim",
            "bnumber" : "B808080",
            "email": "ramazanim@berea.edu",
            "phoneNumber": "(555)555-5555",
            "firstName" : "Ali",
            "lastName" : "Ramazani",
            "isStudent": True,
            "isFaculty": False,
            "isCeltsAdmin": False,
            "isCeltsStudentStaff": False,
            "major": "Computer Science",
            "classLevel": "Senior",
            "minorInterest": 0,
        },
        {
            "username": "einsteina",
            "bnumber": "B00739547",
            "email": "einsteina@berea.edu",
            "phoneNumber": "(555)985-1233",
            "firstName": "Albert",
            "lastName": "Einstein",
            "isStudent": True,
            "isFaculty": False,
            "isCeltsAdmin": False,
            "isCeltsStudentStaff": True,
            "major": "Physics",
            "classLevel": "Sophomore",
            "minorInterest": 0,
        },

        {
            "username" : "lintelmannaders",
            "bnumber": "B00345678",
            "email": "lintelmannaders@berea.edu",
            "phoneNumber": "(555)555-5555",
            "firstName": "Steven",
            "lastName":"Lintelman-Nader",
            "isStudent": True,
            "isFaculty": False,
            "isCeltsAdmin": False,
            "isCeltsStudentStaff": False,
            "major": "Computer Science",
            "classLevel": "Junior",
            "minorInterest": 0,
        },
        {
            "username" : "hamiltonm",
            "bnumber": "B00902854",
            "email": "hamiltonm@berea.edu",
            "phoneNumber": "(220)290-3939",
            "firstName": "Margaret",
            "lastName":"Hamilton",
            "isStudent": True,
            "isFaculty": False,
            "isCeltsAdmin": False,
            "isCeltsStudentStaff": False,
            "major": "Mathematics",
            "classLevel": "Junior",
            "minorInterest": 1,
        },
        {
            "username": "Curiem",
            "bnumber": "B00751180",
            "email": "curiem@berea.edu",
            "firstName": "Marie",
            "lastName": "Curie",
            "isStudent": True,
            "phoneNumber": "(859)433-1559",
            "major": "Chemistry",
            "classLevel": "Senior",
            "minorInterest": 1,

        }]
        User.insert_many(test_usersData).on_conflict_replace().execute()
        yield test_usersData
        transaction.rollback()


@pytest.fixture
def test_eventParticipants():
    with mainDB.atomic() as transaction:
        test_eventParticipantsData = [
        {
            "user": "lintelmannaders",
            "event": 31,
            "hoursEarned": 2
        },
        {
            "user": "Curiem",
            "event": 32,
            "hoursEarned": 2
        },
        {
            "user": "ramazanim",
            "event": 33,
            "hoursEarned": 1
        },
        {
            "user" : "einsteina",
            "event" : 31,
            "hoursEarned" : None,
        },
        {
            "user": "ramazanim",
            "event": 32,
            "hoursEarned": 5
        },
        {
            "user": "hamiltonm",
            "event": 33,
            "hoursEarned": 2,
        },
        {
            "user": "hamiltonm",
            "event": 31,
            "hoursEarned": 3,
        }]
        User.insert_many(test_eventParticipantsData).on_conflict_replace().execute()
        yield test_eventParticipantsData
        transaction.rollback()



@pytest.mark.integration
@pytest.fixture
def fixture_eventData():
    with mainDB.atomic() as transaction:
        test_eventsData = [
        {
            "id": 31,
            "term": 2,
            "name": "Empty Bowls Spring Event 1",
            "description": "Empty Bowls Spring 2021",
            "isTraining": True,
            "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
            "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
            "location": "Seabury Center",
            "startDate": datetime.strptime("2021 10 12","%Y %m %d"),
            "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
            "contactEmail": "testEmail",
            "contactName": "testName",
            "program": 1
            
        },
        {
            "id": 32,
            "term": 2,
            "name": "Hunger Hurts",
            "description": "Will donate Food to Community",
            "isTraining": False,
            "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
            "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
            "location": "Berea Community School",
            "startDate": datetime.strptime("2021 11 12","%Y %m %d"),
            "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
            "contactEmail": "testEmail",
            "contactName": "testName",
            "program": 1
            
        },
        {
            "id": 33,
            "term": 1,
            "name": "Adoption 101",
            "description": "Lecture on adoption",
            "isTraining": True,
            "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
            "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
            "location": "Alumni Patio",
            "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
            "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
            "contactEmail": "testEmail",
            "contactName": "testName",
            "program": 3
        }]
        User.insert_many(test_eventsData).on_conflict_replace().execute()
        yield test_eventsData
        transaction.rollback()


@pytest.mark.integration
@pytest.fixture
def fixture_term():
        with mainDB.atomic() as transaction:
            test_termData = [
            {
            "id": 1,
            "description": "Fall 2020",
            "year": 2020,
            "academicYear": "2020-2021",
            "isSummer": False,
            "isCurrentTerm": False,
            "termOrder": "2020-3"
            },
            {
            "id": 2,
            "description": "Spring 2021",
            "year": 2021,
            "academicYear": "2020-2021",
            "isSummer": False,
            "isCurrentTerm": False,
            "termOrder": "2021-1"
            }]
            User.insert_many(test_termData).on_conflict_replace().execute()
            yield test_termData
            transaction.rollback()


@pytest.mark.integration
def test_createSpreadsheet():
    createSpreadsheet("2020-2021")

@pytest.mark.integration
def test_calculateRetentionRate():
    # Takes 2 dictionaries, a fall and spring dictionary and see who has returned in the spring from the fall term
    fallDict = ({'Adopt-a-Grandparent': ['ramazanim'], 'CELTS-Sponsored Event': [None]})
    springDict = ({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'partont']})
    assert calculateRetentionRate(fallDict, springDict) == {'Adopt-a-Grandparent': 0.0, 'CELTS-Sponsored Event': 0.0}

    fallDict = ({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'partont']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 1.0}

    fallDict = ({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'partont']})
    springDict = ({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 0.75}

@pytest.mark.integration
def test_removeNullParticipants():
    #Removes empty elements fromm a list
    testInputList = ['khatts']
    assert removeNullParticipants(testInputList) == ['khatts']
    testInputList = ['khatts', '', 'ayisie']
    assert removeNullParticipants(testInputList) == ['khatts', 'ayisie']

@pytest.mark.integration
def test_termParticipation(term):
    # Checks who all participated in any given program for an even. NONE will be the result if there was an event for a program without and participants.
    with mainDB.atomic() as transaction:    
        assert termParticipation('Fall 2020') == {'Adopt-a-Grandparent': ['khatts'], 'CELTS-Sponsored Event': [None]}

        EventParticipant.create(user = 'partont',
                                event = 10,
                                hoursEarned = 1)
        termParticipationResult = termParticipation('Fall 2020')
        for participantList in termParticipationResult.values():
            participantList.sort()
        assert termParticipationResult == {'Adopt-a-Grandparent': ['khatts', 'partont'], 'CELTS-Sponsored Event': [None]}

        EventParticipant.create(user = 'ayisie',
                                event = 14,
                                hoursEarned = 1)
        termParticipationResult = termParticipation('Fall 2020')
        for participantList in termParticipationResult.values():
            participantList.sort()
        assert termParticipationResult == {'Adopt-a-Grandparent': ['khatts', 'partont'], 'CELTS-Sponsored Event': ['ayisie']}
        transaction.rollback()

@pytest.mark.integration
def test_getRetentionRate():
    #Takes an academic year and returns how many people were retained across terms by percentage for each program.
    with mainDB.atomic() as transaction:
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        testProgram = Program.create(programName = "Test Program",
                                     programDescription = "A good program")
        fallEvent = Event.create(name="Fall2020Event",
                                 term=1, #Fall 2020
                                 program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=fallEvent,
                                hoursEarned=1)
        assert sorted(getRetentionRate("2020-2021")) == [('Adopt-a-Grandparent', '0.0%'), 
                                                         ('CELTS-Sponsored Event', '0.0%'), 
                                                         ('Test Program', '0.0%')]
        
        springEvent = Event.create(name="Spring2021Event",
                                  term=2, #Spring 2021
                                  program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=springEvent,
                                hoursEarned=1)
        assert sorted(getRetentionRate("2020-2021")) == [('Adopt-a-Grandparent', '0.0%'), 
                                                         ('CELTS-Sponsored Event', '0.0%'), 
                                                         ('Test Program', '100.0%')]
        transaction.rollback()

@pytest.mark.integration
def test_repeatVolunteers(term):
    #repeat volunteers people who participated in more than one event
    with mainDB.atomic() as transaction:
        EventParticipant.delete().execute()
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        testProgram = Program.create(programName = "Test Program",
                                     programDescription = "A good program")
        testEvent = Event.create(name="Fall2020Event",
                                 term=term.id,
                                 program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteers(term.academicYear))) == []
        testEvent2 = Event.create(name="Spring2021Event",
                                 term=term.id,
                                 program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent2,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteers(term.academicYear))) == [('Madinabonu Solijonova', 2)]
        EventParticipant.delete().execute()
        assert sorted(list(repeatVolunteers(term.academicYear))) == []
        EventParticipant.create(user='solijonovam',
                                event=testEvent,
                                hoursEarned=1)
        testDifferentProgram = Program.create(programName = "Test Program 2",
                                              programDescription = "A good program")
        testEvent2 = Event.create(name="Spring2021Event",
                                  term=term.id,
                                  program=testDifferentProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent2,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteers(term.academicYear))) == [('Madinabonu Solijonova', 2)]
        transaction.rollback()

@pytest.mark.integration
def test_repeatVolunteersPerProgram(term):
    print("###@", term)
    # Find people who have participated in two events of the same program
    with mainDB.atomic() as transaction:
        EventParticipant.delete().execute()
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        testProgram = Program.create(programName = "Test Program",
                                     programDescription = "A good program")
        testEvent = Event.create(name="Test Event",
                                 term=term.id, 
                                 program=testProgram,
                                 
                                 )
        EventParticipant.create(user='solijonovam',
                                event=testEvent,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteersPerProgram(term.academicYear))) == []
        testProgram2 = Program.create(programName = "Test Program 2",
                                     programDescription = "A good program")
        testEvent2 = Event.create(name="Test Event2",
                                 term=term.id, 
                                 program=testProgram2)
        EventParticipant.create(user='solijonovam',
                                event=testEvent2,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteersPerProgram(term.academicYear))) == []
        testEvent3 = Event.create(name="Test Event3",
                                 term=term.id, 
                                 program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent3,
                                hoursEarned=1)
        assert sorted(list(repeatVolunteersPerProgram(term.academicYear))) == [('Madinabonu Solijonova', 'Test Program', 2)]

        transaction.rollback()

@pytest.mark.integration
def test_volunteerMajorAndClass(term, user): 
    # Gets the list of majors or the class levels of volunteers
    with mainDB.atomic() as transaction:
        print(term.academicYear, User.major)

        print("tsst", list(volunteerMajorAndClass(term.academicYear, User.classLevel)))
        assert list(volunteerMajorAndClass(term.academicYear, User.major)) == list([('Chemistry', 1), ('Computer Science', 2), ('Psychology', 1)])
        assert list(volunteerMajorAndClass(term.academicYear, User.classLevel)) == [('Junior', 1), ('Senior', 2), ('Sophomore', 1)]
        assert list(volunteerMajorAndClass(term.academicYear, User.classLevel, True)) == [('Sophomore', 1), ('Junior', 1), ('Senior', 3)]

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
                                event = 2,
                                hoursEarned = 2,
                                )
        Term.create(academicYear = "2020-2021", 
                    id = 1 
                    )
        Event.create(term = 1)
        assert list(volunteerMajorAndClass("2020-2021", User.major)) == [('Agriculture', 1), ('Biology', 1), ('Chemistry', 1), ('Computer Science', 2), ('Psychology', 1)]
        assert list(volunteerMajorAndClass("2020-2021", User.classLevel)) == [('Junior', 1), ('Senior', 3), ('Sophomore', 2)]
        assert list(volunteerMajorAndClass("2020-2021", User.classLevel, True)) == [('Sophomore', 2), ('Junior', 1), ('Senior', 3)]
        transaction.rollback()

@pytest.mark.integration
def test_volunteerHoursByProgram():
    # Gets the list of volunteer hours per program as a tuple
    with mainDB.atomic() as transaction:
        EventParticipant.delete().execute()
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
        testProgram = Program.create(programName = "Test Program",
                                     programDescription = "A good program")
        testEvent = Event.create(name="Test Event",
                                 term=3,
                                 program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent,
                                hoursEarned=2
                                )
        testEvent2 = Event.create(name="Test Event",
                                  term=2,
                                  program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent2,
                                hoursEarned=3
                                )
        testEvent3 = Event.create(name="Test Event",
                                  term=4,
                                  program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent3,
                                hoursEarned=5
                                )
        assert list(volunteerHoursByProgram()) == [('Test Program', 10.0)]
        transaction.rollback()

@pytest.mark.integration
def test_onlyCompletedAllVolunteer():
    # This function returns a list of usernames and fullnames for people who have only completed all volunteer training in a particular academic year.
    with mainDB.atomic() as transaction:
        assert list(onlyCompletedAllVolunteer("2020-2021")) == []
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        
        allVolunteerEvent = Event.create(name="All Volunteer Training",
                                 term=1,
                                 program=9,
                                 isTraining=1,
                                 isAllVolunteerTraining=1)
        EventParticipant.create(user = 'solijonovam', # Not participated in event
                                event = allVolunteerEvent, # Added to all volunteer training event
                                hoursEarned = 1)
        assert list(onlyCompletedAllVolunteer("2020-2021")) == [('solijonovam', 'Madinabonu Solijonova')]
        testEvent = Event.create(name="Test Event",
                                  program=1,
                                  term=1)
        EventParticipant.create(user = 'solijonovam', # Only participated in all volunteer event
                                event = testEvent,
                                hoursEarned = 1)
        assert list(onlyCompletedAllVolunteer("2020-2021")) == []
        transaction.rollback()

@pytest.mark.integration
def test_volunteerProgramHours():
    # Returns list of (program, username, hours) for each program
    with mainDB.atomic() as transaction:
        EventParticipant.delete().execute()
        assert sorted(list(volunteerProgramHours())) == ([])
        EventParticipant.create(user = 'qasema',
                                event = 2,
                                hoursEarned = 1)
        assert sorted(list(volunteerProgramHours())) == [('Hunger Initiatives', 'qasema', 1.0)]
        EventParticipant.create(user = 'qasema',
                                event = 3,
                                hoursEarned = 1)
        assert sorted(list(volunteerProgramHours())) == [('Adopt-a-Grandparent', 'qasema', 1.0), ('Hunger Initiatives', 'qasema', 1.0)]
        transaction.rollback()

@pytest.mark.integration
def test_totalVolunteerHours(term):
    #Returns the total amount of volunteer hours in the database
    with mainDB.atomic() as transaction:
        EventParticipant.delete().execute()
        Event.delete().execute()
        Term.delete().execute()

        Term.create(id = 1,
                    academicYear = '2021-2022',)
        
        assert list(totalVolunteerHours(term)) == [(None,)]
        # Adding 1 volunteer hour to one event
        Event.create(id = 2, 
                     term_id = 1,)
        EventParticipant.create(user = 'qasema',
                                event = 2,
                                hoursEarned = 1)
        # Checking that the total volunteer hours has increased by 1
        assert list(totalVolunteerHours(term)) == [(1.0,)]
        EventParticipant.create(user = 'ayisie',
                                event = 3,
                                hoursEarned = 6)
        assert list(totalVolunteerHours(term)) == [(7.0,)]
        transaction.rollback()

@pytest.mark.integration
def test_getVolunteerProgramEventByTerm():
    # Returns a list for every eventparticipant entry for (full name, username, program, and event) for a given term
    with mainDB.atomic() as transaction:
        assert list(getVolunteerProgramEventByTerm(Term.get_by_id(3))) == ([])
        assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(2)))) == ([('Ebenezer Ayisi', 'ayisie', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
                                                                                    ('Sreynit Khatt', 'khatts', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
                                                                                    ('Tyler Parton', 'partont', 'Hunger Initiatives', 'Hunger Hurts'),
                                                                                    ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
                                                                                    ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Hunger Hurts')])

        assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(4)))) == [('Alex Bryant', 'bryanta', 'Berea Buddies', 'Tutoring'),
                                                                                   ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Adoption 101'),
                                                                                   ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Meet & Greet with Grandparent')]
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        testProgram = Program.create(programName = "Test Program",
                                     programDescription = "A good program")
        testEvent = Event.create(name="Test Event",
                                 term=3,
                                 program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent)
        testEvent2 = Event.create(name="Test Event",
                                  term=2,
                                  program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent2)
        testEvent3 = Event.create(name="Test Event",
                                  term=4,
                                  program=testProgram)
        EventParticipant.create(user='solijonovam',
                                event=testEvent3)
        assert list(getVolunteerProgramEventByTerm(Term.get_by_id(3))) == [('Madinabonu Solijonova', 'solijonovam', 'Test Program', 'Test Event')]
        assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(2)))) == [('Ebenezer Ayisi', 'ayisie', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
                                                                                   ('Madinabonu Solijonova', 'solijonovam', 'Test Program', 'Test Event'),
                                                                                   ('Sreynit Khatt', 'khatts', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
                                                                                   ('Tyler Parton', 'partont', 'Hunger Initiatives', 'Hunger Hurts'), 
                                                                                   ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
                                                                                   ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Hunger Hurts')]

        assert sorted(list(getVolunteerProgramEventByTerm(Term.get_by_id(4)))) == [('Alex Bryant', 'bryanta', 'Berea Buddies', 'Tutoring'), 
                                                                                   ('Madinabonu Solijonova', 'solijonovam', 'Test Program', 'Test Event'),
                                                                                   ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Adoption 101'), 
                                                                                   ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Meet & Greet with Grandparent')]
        transaction.rollback()

@pytest.mark.integration
def test_getUniqueVolunteers():
    # Returns a list of everyone who has volunteered.
    with mainDB.atomic() as transaction:
        assert sorted(list(getUniqueVolunteers("2021-2022"))) == ([('bryanta', 'Alex Bryant', 'B00708826'),
                                                                   ('khatts', 'Sreynit Khatt', 'B00759107')])
    
        assert sorted(list(getUniqueVolunteers("2020-2021"))) == ([('ayisie', 'Ebenezer Ayisi', 'B00739736'),
                                                                   ('khatts', 'Sreynit Khatt', 'B00759107'),
                                                                   ('neillz', 'Zach Neill', 'B00751864'),
                                                                   ('partont', 'Tyler Parton', 'B00751360')])
        
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        testEvent = Event.create(name="Test Event",
                                 term=1,
                                 program=1)
        EventParticipant.create(user = 'solijonovam',
                                event = testEvent,
                                hoursEarned = 1)
        
        assert sorted(list(getUniqueVolunteers("2020-2021"))) == [('ayisie', 'Ebenezer Ayisi', 'B00739736'), 
                                                                  ('khatts', 'Sreynit Khatt', 'B00759107'), 
                                                                  ('neillz', 'Zach Neill', 'B00751864'), 
                                                                  ('partont', 'Tyler Parton', 'B00751360'), 
                                                                  ('solijonovam', 'Madinabonu Solijonova', 'B00769465')]
        transaction.rollback()
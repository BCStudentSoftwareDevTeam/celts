import pytest
from datetime import date
from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.logic.volunteerSpreadsheet import *
from app.models.program import Program
from app.models.event import Event

@pytest.fixture
def fixture_info():
    with mainDB.atomic() as transaction:
        user1 = User.create(username="doej", firstName="John", lastName="Doe", bnumber="B774377", major="Graphics Design", rawClassLevel="Sophomore")
        user2 = User.create(username="doej2", firstName="Jane", lastName="Doe", bnumber="B888828", major="Biology", rawClassLevel="Junior")
        user3 = User.create(username="builderb", firstName="Bob", lastName="Builder", bnumber="B00700932", major="Construction", rawClassLevel="Senior")

        term1 = Term.create(description='Fall 2023', academicYear='2023-2024-test')
        term2 = Term.create(description='Fall 2024', academicYear='2024-2025-test')
        term3 = Term.create(description='Spring 2024', academicYear='2023-2024-test')
        term4 = Term.create(description='Spring 2025', academicYear='2024-2025-test')

        program1 = Program.create(programName='Program1')
        program2 = Program.create(programName='Program2')
        program3 = Program.create(programName='Program3')
        program4 = Program.create(programName='Program4')

        event1 = Event.create(
            name='Event1',
            term=term1,
            program=program1,
            startDate=date(2023, 9, 1),
            isCanceled=False,
            deletionDate=None,
            isService=True, 
            isLaborOnly=True
        )
        event2 = Event.create(
            name='Event2',
            term=term1,
            program=program2,
            startDate=date(2023, 9, 10),
            isCanceled=False,
            deletionDate=None,
            isService=True, 
            isLaborOnly=True
        )
        event3 = Event.create(
            name='Event3',
            term=term1,
            program=program3,
            startDate=date(2023, 10, 1),
            isCanceled=False,
            deletionDate=None,
            isService=True
        )
        event4 = Event.create(
            name='Event4',
            term=term2,
            program=program4,
            startDate=date(2024, 9, 1),
            isCanceled=False,
            deletionDate=None,
            isService=True
        )


        eventparticipant1 = EventParticipant.create(event=event1, user=user1, hoursEarned=5)
        eventparticipant2 = EventParticipant.create(event=event1, user=user2, hoursEarned=3)
        eventparticipant4 = EventParticipant.create(event=event4, user=user3, hoursEarned=0)

        yield {
            'user1': user1,
            'user2': user2,
            'user3': user3,
            'term1': term1,
            'term2': term2,
            'term3': term3,
            'term4': term4,
            'program1': program1,
            'program2': program2,
            'program3': program3,
            'program4': program4,
            'event1': event1,
            'event2': event2,
            'event3': event3,
            'event4': event4,
            'eventparticipant1': eventparticipant1,
            'eventparticipant2': eventparticipant2,
            'eventparticipant4': eventparticipant4,
        }

        transaction.rollback()


@pytest.mark.integration
def test_createSpreadsheet(fixture_info):
    createSpreadsheet("2023-2024-test")
    createSpreadsheet("2024-2025-test")


@pytest.mark.unit 
def test_calculateRetentionRate():
    # Takes 2 dictionaries, a fall and spring dictionary and see who has returned in the spring from the fall term
    fallDict = ({'Adopt-a-Grandparent': ['curiem'], 'CELTS-Sponsored Event': [None]})
    springDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'doej2']})
    assert calculateRetentionRate(fallDict, springDict) == {'Adopt-a-Grandparent': 0.0, 'CELTS-Sponsored Event': 0.0}

    fallDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'doej2']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 1.0}

    springDict = ({'Hunger Initiatives': ['einsteina', 'lintelmannaders', 'doej', 'ayisie']})
    assert calculateRetentionRate(fallDict, springDict) == {'Hunger Initiatives': 0.75}


@pytest.mark.unit
def test_removeNullParticipants():
    #Removes empty elements fromm a list
    testInputList = ['khatts']
    assert removeNullParticipants(testInputList) == ['khatts']
    testInputList = ['khatts', '', 'ayisie']
    assert removeNullParticipants(testInputList) == ['khatts', 'ayisie']


@pytest.mark.integration
def test_termParticipation(fixture_info):
    # Checks who all participated in any given program for an even. NONE will be the result if there was an event for a program without and participants.
    assert termParticipation(fixture_info['term1']) == {'Program1': ['doej', 'doej2']}
    assert termParticipation(fixture_info['term2']) == {'Program4': ['builderb']}

    EventParticipant.create(user = fixture_info['user3'],
                            event = fixture_info['event1'],
                            hoursEarned = 1)
    termParticipationResult = termParticipation(fixture_info["term1"])
    for participantList in termParticipationResult.values():
        participantList.sort()
    assert termParticipationResult == {'Program1': ['builderb', 'doej', 'doej2']}

    EventParticipant.create(user = fixture_info['user3'],
                            event = fixture_info['event2'],
                            hoursEarned = 1)
    termParticipationResult = termParticipation(fixture_info["term1"])
    for participantList in termParticipationResult.values():
        participantList.sort()
    assert termParticipationResult == {'Program1': ['builderb', 'doej', 'doej2'], 
                                       'Program2': ['builderb']}


@pytest.mark.integration
def test_getRetentionRate(fixture_info):
    #Takes an academic year and returns how many people were retained across terms by percentage for each program.

    columns, retention = getRetentionRate("2023-2024-test")

    assert columns == ["Program", "Retention Rate"]
    assert sorted(retention) == [('Program1', '0.0%')]

    columns, retention = getRetentionRate("2024-2025-test")
    assert columns == ["Program", "Retention Rate"]
    assert sorted(retention) == [('Program4', '0.0%')]

    springEvent = Event.create(
        name="Spring2021Event",
        program=fixture_info["program1"],
        term=fixture_info["term3"],  
        startDate=date(2024, 2, 1),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(user=fixture_info['user1'],
                            event=springEvent,
                            hoursEarned=1)
    
    # Check for john doe participating in both semesters
    columns, retention = getRetentionRate("2023-2024-test")
    assert columns == ["Program", "Retention Rate"]
    assert sorted(retention) == [("Program1", "50.0%")]

    # Jane Doe also participates in spring so 2 of 2 retained = 100%
    EventParticipant.create(user=fixture_info['user2'],
                            event=springEvent,
                            hoursEarned=1)
    
    columns, retention = getRetentionRate("2023-2024-test")
    assert columns == ["Program", "Retention Rate"]
    assert sorted(retention) == [("Program1", "100.0%")]


@pytest.mark.integration
def test_repeatParticipants(fixture_info):
    # repeatParticipants  people who have more than 1 EventParticipant row in the academic year

    # Add a second participation for John Doe in the same academic year as term1
    testEvent = Event.create(
        name="Test Event",
        term=fixture_info["term1"],
        program=fixture_info["program1"],
        startDate=date(2023, 11, 1),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )
    EventParticipant.create(
        user=fixture_info["user1"],
        event=testEvent,
        hoursEarned=1
    )

    columns, rows = repeatParticipants("2023-2024-test")
    assert columns == ["Number of Events", "Full Name", "Email", "B-Number"]
    assert list(rows) == [(2, "John Doe", "doej@berea.edu", "B774377")]

    columns, rows = repeatParticipants("2024-2025-test")
    assert columns == ["Number of Events", "Full Name", "Email", "B-Number"]
    assert list(rows) == []

    # Add a third participation for John Doe (another separate event)
    testEvent2 = Event.create(
        name="Test Event 2",
        term=fixture_info["term1"],
        program=fixture_info["program2"],
        startDate=date(2023, 11, 2),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )
    EventParticipant.create(
        user=fixture_info["user1"],
        event=testEvent2,
        hoursEarned=0
    )

    columns, rows = repeatParticipants("2023-2024-test")
    assert list(rows) == [(3, "John Doe", "doej@berea.edu", "B774377")]



@pytest.mark.integration
def test_repeatParticipantsPerProgram(fixture_info):
    # repeatParticipantsPerProgram = people who participated in more than 1 event of the same program

    columns, rows = repeatParticipantsPerProgram("2023-2024-test")
    assert columns == ["Volunteer", "Program Name", "Event Count"]
    assert list(rows) == []

    # Add second event for Program1 for John Doe
    testEvent3 = Event.create(
        name="Test Event",
        term=fixture_info['term1'],
        program=fixture_info['program1'],
        startDate=date(2023, 11, 5),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(
        user=fixture_info['user1'],
        event=testEvent3,
        hoursEarned=1
    )

    columns, rows = repeatParticipantsPerProgram("2023-2024-test")
    assert list(rows) == [("John Doe", "Program1", 2)]

    # Add third event for same program
    testEvent4 = Event.create(
        name="Test Event 2",
        term=fixture_info['term1'],
        program=fixture_info['program1'],
        startDate=date(2023, 11, 6),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(
        user=fixture_info['user1'],
        event=testEvent4,
        hoursEarned=1
    )

    columns, rows = repeatParticipantsPerProgram("2023-2024-test")
    assert list(rows) == [("John Doe", "Program1", 3)]


@pytest.mark.integration
def test_volunteerMajorAndClass(fixture_info):
    # volunteerMajorAndClass now returns (columns, rows)

    columns, rows = volunteerMajorAndClass("2023-2024-test", User.major)
    assert columns == ["Major", "Count"]
    assert list(rows) == [("Biology", 1), ("Graphics Design", 1)]

    columns, rows = volunteerMajorAndClass("2023-2024-test", User.rawClassLevel)
    assert columns == ["Major", "Count"]
    assert list(rows) == [("Junior", 1), ("Sophomore", 1)]

    columns, rows = volunteerMajorAndClass("2023-2024-test", User.rawClassLevel, True)
    assert columns == ["Class Level", "Count"]
    assert list(rows) == [("Sophomore", 1), ("Junior", 1)]

    columns, rows = volunteerMajorAndClass("2024-2025-test", User.major)
    assert columns == ["Major", "Count"]
    assert list(rows) == [("Construction", 1)]

    columns, rows = volunteerMajorAndClass("2024-2025-test", User.rawClassLevel)
    assert columns == ["Major", "Count"]
    assert list(rows) == [("Senior", 1)]

    columns, rows = volunteerMajorAndClass("2024-2025-test", User.rawClassLevel, True)
    assert columns == ["Class Level", "Count"]
    assert list(rows) == [("Senior", 1)]

    # Add a new user and make them participate in a service event in 2023-2024-test
    newUser = User.create(
        username="solijonovam_test",
        email="solijonovam@berea.edu",
        firstName="Madinabonu",
        lastName="Solijonova",
        major="Agriculture",
        rawClassLevel="Sophomore"
    )

    EventParticipant.create(
        user=newUser,
        event=fixture_info["event1"],
        hoursEarned=2
    )

    # Add user3 to the same event so Construction major becomes part of 2023-2024-test service participants too
    EventParticipant.create(
        user=fixture_info["user3"],
        event=fixture_info["event1"],
        hoursEarned=3
    )

    columns, rows = volunteerMajorAndClass("2023-2024-test", User.major)
    assert columns == ["Major", "Count"]
    assert list(rows) == [("Agriculture", 1), ("Biology", 1), ("Construction", 1), ("Graphics Design", 1)]

    columns, rows = volunteerMajorAndClass("2023-2024-test", User.rawClassLevel)
    assert columns == ["Major", "Count"]
    assert sorted(list(rows)) == sorted([("Junior", 1), ("Senior", 1), ("Sophomore", 2)])

    columns, rows = volunteerMajorAndClass("2023-2024-test", User.rawClassLevel, True)
    assert columns == ["Class Level", "Count"]
    assert list(rows) == [("Sophomore", 2), ("Junior", 1), ("Senior", 1)]



@pytest.mark.integration
def test_totalHoursByProgram(fixture_info):
    # totalHoursByProgram returns (columns, rows)
    # columns = ["Program", "Service Hours", "Training Hours", "Other Hours"]

    columns, rows = totalHoursByProgram("2023-2024-test")
    assert columns == ["Program", "Service Hours", "Training Hours", "Other Hours"]
    assert list(rows) == [("Program1", 8.0, 0.0, 0.0)]

    columns, rows = totalHoursByProgram("2024-2025-test")
    assert columns == ["Program", "Service Hours", "Training Hours", "Other Hours"]
    assert list(rows) == [("Program4", 0.0, 0.0, 0.0)]

    # Add more service hours in Program1 in 2023-2024-test
    EventParticipant.create(
        event=fixture_info["event1"],
        user=fixture_info["user3"],
        hoursEarned=10
    )

    columns, rows = totalHoursByProgram("2023-2024-test")
    assert list(rows) == [("Program1", 18.0, 0.0, 0.0)]


@pytest.mark.integration
def test_onlyCompletedAllVolunteer(fixture_info):
    # onlyCompletedAllVolunteer returns (columns, rows)

    columns, rows = onlyCompletedAllVolunteer("2023-2024-test")
    assert columns == ["Full Name", "Email", "B-Number"]
    assert list(rows) == []

    allVolunteerEvent = Event.create(
        name="All Volunteer Training",
        term=fixture_info["term1"],
        program=fixture_info["program1"],
        startDate=date(2023, 9, 20),
        isCanceled=False,
        deletionDate=None,
        isService=False,
        isTraining=True,
        isAllVolunteerTraining=True
    )

    EventParticipant.create(
        user=fixture_info["user3"],
        event=allVolunteerEvent,
        hoursEarned=1
    )

    columns, rows = onlyCompletedAllVolunteer("2023-2024-test")
    assert list(rows) == [("Bob Builder", "builderb@berea.edu", "B00700932")]

    columns, rows = onlyCompletedAllVolunteer("2024-2025-test")
    assert list(rows) == []

    # Now Bob participates in a service event too, so he should be removed
    testEvent = Event.create(
        name="Test Service Event",
        program=fixture_info["program1"],
        term=fixture_info["term1"],
        startDate=date(2023, 9, 21),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(
        user=fixture_info["user3"],
        event=testEvent,
        hoursEarned=1
    )

    columns, rows = onlyCompletedAllVolunteer("2023-2024-test")
    assert list(rows) == []


@pytest.mark.integration
def test_volunteerProgramHours(fixture_info):
    # volunteerProgramHours returns (columns, rows)
    columns, rows = volunteerProgramHours("2023-2024-test")
    assert columns == ["Program Name", "Volunteer Hours", "Volunteer Name", "Volunteer Email", "Volunteer B-Number"]
    assert sorted(list(rows)) == sorted([
        ("Program1", 5.0, "John Doe", "doej@berea.edu", "B774377"),
        ("Program1", 3.0, "Jane Doe", "doej2@berea.edu", "B888828"),
    ])

    columns, rows = volunteerProgramHours("2024-2025-test")
    assert columns == ["Program Name", "Volunteer Hours", "Volunteer Name", "Volunteer Email", "Volunteer B-Number"]
    assert list(rows) == [
        ("Program4", 0.0, "Bob Builder", "builderb@berea.edu", "B00700932")
    ]

    # Add John to event2 (Program2) for 1 hour
    EventParticipant.create(
        user=fixture_info["user1"],
        event=fixture_info["event2"],
        hoursEarned=1
    )

    columns, rows = volunteerProgramHours("2023-2024-test")
    assert sorted(list(rows)) == sorted([
        ("Program1", 5.0, "John Doe", "doej@berea.edu", "B774377"),
        ("Program1", 3.0, "Jane Doe", "doej2@berea.edu", "B888828"),
        ("Program2", 1.0, "John Doe", "doej@berea.edu", "B774377"),
    ])

    # Add another Program1 event for John for 2 hours (so Program1 John becomes 7 total)
    testEvent = Event.create(
        name="Extra Program1 Event",
        program=fixture_info["program1"],
        term=fixture_info["term1"],
        startDate=date(2023, 11, 10),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(
        user=fixture_info["user1"],
        event=testEvent,
        hoursEarned=2
    )

    columns, rows = volunteerProgramHours("2023-2024-test")
    assert sorted(list(rows)) == sorted([
        ("Program1", 7.0, "John Doe", "doej@berea.edu", "B774377"),
        ("Program1", 3.0, "Jane Doe", "doej2@berea.edu", "B888828"),
        ("Program2", 1.0, "John Doe", "doej@berea.edu", "B774377"),
    ])


@pytest.mark.integration
def test_totalHours(fixture_info):
    # totalHours returns (columns, rows)
    columns, rows = totalHours("2023-2024-test")
    assert columns == ["Total Service Hours", "Total Training Hours", "Other Participation Hours"]
    assert list(rows) == [(8.0, 0.0, 0.0)]

    columns, rows = totalHours("2024-2025-test")
    assert columns == ["Total Service Hours", "Total Training Hours", "Other Participation Hours"]
    assert list(rows) == [(0.0, 0.0, 0.0)]

    # Add a participant with 0 hours (should not change totals)
    EventParticipant.create(
        user=fixture_info["user3"],
        event=fixture_info["event3"],
        hoursEarned=0
    )

    columns, rows = totalHours("2023-2024-test")
    assert list(rows) == [(8.0, 0.0, 0.0)]

    columns, rows = totalHours("2024-2025-test")
    assert list(rows) == [(0.0, 0.0, 0.0)]

    # Add 1 volunteer hour to event2 (service event in 2023-2024-test)
    EventParticipant.create(
        user=fixture_info["user3"],
        event=fixture_info["event2"],
        hoursEarned=1
    )

    columns, rows = totalHours("2023-2024-test")
    assert list(rows) == [(9.0, 0.0, 0.0)]

    # Add 3 more service hours to event1 for user1
    EventParticipant.create(
        user=fixture_info["user1"],
        event=fixture_info["event1"],
        hoursEarned=3
    )

    columns, rows = totalHours("2023-2024-test")
    assert list(rows) == [(12.0, 0.0, 0.0)]


@pytest.mark.integration
def test_getAllTermData(fixture_info):
    # getAllTermData(term) returns (columns, rows)

    def rows_as_dicts(columns, rows):
        dict_list = []
        for row in rows:
            dict_list.append(dict(zip(columns, row)))
        return dict_list

    # TERM 1 should include Event1 participation for John + Jane
    columns, rows = getAllTermData(fixture_info["term1"])
    data = rows_as_dicts(columns, rows)

    # John in Event1
    johnEvent1= [
        r for r in data
        if r["Event Name"] == "Event1" and r["Student Email"] == "doej@berea.edu"
    ]
    assert len(johnEvent1) == 1
    assert johnEvent1[0]["Program Name"] == "Program1"
    assert johnEvent1[0]["Hours Earned"] == 5

    # Jane in Event1
    janeEvent1 = [
        r for r in data
        if r["Event Name"] == "Event1" and r["Student Email"] == "doej2@berea.edu"
    ]
    assert len(janeEvent1) == 1
    assert janeEvent1[0]["Program Name"] == "Program1"
    assert janeEvent1[0]["Hours Earned"] == 3

    # TERM 2 should include Event4 participation for Bob
    columns, rows = getAllTermData(fixture_info["term2"])
    data = rows_as_dicts(columns, rows)

    bobEvent4 = [
        r for r in data
        if r["Event Name"] == "Event4" and r["Student Email"] == "builderb@berea.edu"
    ]
    assert len(bobEvent4) == 1
    assert bobEvent4[0]["Program Name"] == "Program4"
    assert bobEvent4[0]["Hours Earned"] == 0

    # Add Bob to Event2 (term1) with 0 hours, should show up in term1 data
    EventParticipant.create(
        user=fixture_info["user3"],
        event=fixture_info["event2"],
        hoursEarned=0
    )

    # Also add John to Event2 so he appears under Program2
    EventParticipant.create(
        user=fixture_info["user1"],
        event=fixture_info["event2"],
        hoursEarned=0
    )

    columns, rows = getAllTermData(fixture_info["term1"])
    data = rows_as_dicts(columns, rows)

    bobEvent2 = [
        r for r in data
        if r["Event Name"] == "Event2" and r["Student Email"] == "builderb@berea.edu"
    ]
    assert len(bobEvent2) == 1
    assert bobEvent2[0]["Program Name"] == "Program2"
    assert bobEvent2[0]["Hours Earned"] == 0

    # Create two more Program2 events in term1 and add John to both
    testEvent = Event.create(
        name="Test Event",
        term=fixture_info["term1"],
        program=fixture_info["program2"],
        startDate=date(2023, 11, 20),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )
    testEvent2 = Event.create(
        name="Test Event 2",
        term=fixture_info["term1"],
        program=fixture_info["program2"],
        startDate=date(2023, 11, 21),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(user=fixture_info["user1"], event=testEvent, hoursEarned=0)
    EventParticipant.create(user=fixture_info["user1"], event=testEvent2, hoursEarned=0)

    columns, rows = getAllTermData(fixture_info["term1"])
    data = rows_as_dicts(columns, rows)

    johnProgram2Events= [
        r for r in data
        if r["Student Email"] == "doej@berea.edu" and r["Program Name"] == "Program2"
    ]
    eventNames = sorted([r["Event Name"] for r in johnProgram2Events])
    assert eventNames == ["Event2", "Test Event", "Test Event 2"]

@pytest.mark.integration
def test_getUniqueVolunteers(fixture_info):
    columns, rows = getUniqueVolunteers("2023-2024-test")
    assert columns == ["Full Name", "Email", "B-Number"]
    assert sorted(list(rows)) == sorted([
        ("John Doe", "doej@berea.edu", "B774377"),
        ("Jane Doe", "doej2@berea.edu", "B888828"),
    ])

    columns, rows = getUniqueVolunteers("2024-2025-test")
    assert list(rows) == [
        ("Bob Builder", "builderb@berea.edu", "B00700932")
    ]

    # Add Bob to a 2023-2024 service event so he becomes a unique volunteer for that year too
    EventParticipant.create(
        user=fixture_info["user3"],
        event=fixture_info["event1"],
        hoursEarned=0
    )

    columns, rows = getUniqueVolunteers("2023-2024-test")
    assert sorted(list(rows)) == sorted([
        ("Bob Builder", "builderb@berea.edu", "B00700932"),
        ("John Doe", "doej@berea.edu", "B774377"),
        ("Jane Doe", "doej2@berea.edu", "B888828"),
    ])

    # Add a new user + a service participation in term1
    User.create(username="testt", firstName="Test", lastName="Tester", bnumber="B55555")

    testEvent = Event.create(
        name="Test Event",
        term=fixture_info["term1"],
        program=fixture_info["program1"],
        startDate=date(2023, 12, 1),
        isCanceled=False,
        deletionDate=None,
        isService=True
    )

    EventParticipant.create(
        user="testt",
        event=testEvent,
        hoursEarned=1
    )

    columns, rows = getUniqueVolunteers("2023-2024-test")
    assert sorted(list(rows)) == sorted([
        ("Bob Builder", "builderb@berea.edu", "B00700932"),
        ("John Doe", "doej@berea.edu", "B774377"),
        ("Jane Doe", "doej2@berea.edu", "B888828"),
        ("Test Tester", "testt@berea.edu", "B55555"),
    ])

@pytest.mark.integration
def test_laborAttendanceByTerm(fixture_info):
    EventParticipant.create(event=fixture_info["event1"], user=fixture_info['user1'], hoursEarned=1)
    EventParticipant.create(event=fixture_info["event2"], user=fixture_info['user1'], hoursEarned=1)
    EventParticipant.create(event=fixture_info["event1"], user=fixture_info['user2'], hoursEarned=1)

    columns, results = laborAttendanceByTerm("2023-2024-test")
    assert columns == ("Full Name", "B-Number", "Email", "Term", "Meetings Attended")

    assert len(results) == 2
    assert ("John Doe", "B774377", "doej@berea.edu", "Fall 2023", 3) in results
    assert ("Jane Doe", "B888828", "doej2@berea.edu", "Fall 2023", 2) in results
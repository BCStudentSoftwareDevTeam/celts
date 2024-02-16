import pytest

from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant

from app.logic.spreadsheet import *


@pytest.mark.integration
def test_create_spreadsheet():
    create_spreadsheet("2020-2021")

@pytest.mark.integration
def test_calculateRetentionRate():
    fall_dict=({'Adopt-a-Grandparent': ['khatts'], 'CELTS-Sponsored Event': [None]})
    spring_dict=({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'partont']})
    assert calculateRetentionRate(fall_dict,spring_dict) == {'Adopt-a-Grandparent': 0.0, 'CELTS-Sponsored Event': 0.0}

    fall_dict=({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'partont']})
    assert calculateRetentionRate(fall_dict,spring_dict) == {'Hunger Initiatives': 1.0}

    fall_dict=({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'partont']})
    spring_dict=({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie']})
    assert calculateRetentionRate(fall_dict,spring_dict) == {'Hunger Initiatives': 0.75}

@pytest.mark.integration
def test_removeNullParticipants():
    test_input_list = ['khatts']
    assert removeNullParticipants(test_input_list) == ['khatts']
    test_input_list = ['khatts', '', 'ayisie']
    assert removeNullParticipants(test_input_list) == ['khatts', 'ayisie']

@pytest.mark.integration
def test_termParticipation():
    with mainDB.atomic() as transaction:    
        assert termParticipation('Fall 2020')=={'Adopt-a-Grandparent': ['khatts'], 'CELTS-Sponsored Event': [None]}

        EventParticipant.create(user = 'partont',
                                event = 10,
                                hoursEarned = 1)
        assert termParticipation('Fall 2020')=={'Adopt-a-Grandparent': ['khatts', 'partont'], 'CELTS-Sponsored Event': [None]}

        EventParticipant.create(user = 'ayisie',
                                event = 14,
                                hoursEarned = 1)
        assert termParticipation('Fall 2020')=={'Adopt-a-Grandparent': ['khatts', 'partont'], 'CELTS-Sponsored Event': ['ayisie']}
        transaction.rollback()

@pytest.mark.integration
def test_getRetentionRate():
    with mainDB.atomic() as transaction:
        assert getRetentionRate("2020-2021") == [('Adopt-a-Grandparent', '0.0%'), ('CELTS-Sponsored Event', '0.0%')]
        
        testEvent = Event.create(name="Test Event",
                                 term=2,
                                 program=3) #Adopt a grandparent program
        EventParticipant.create(user = 'khatts', #Adding khatts to Spring term since they have participated in an ebent in the same program in the Fall term
                                event = testEvent,
                                hoursEarned = 1)
        assert getRetentionRate("2020-2021") == [('Adopt-a-Grandparent', '100.0%'), ('CELTS-Sponsored Event', '0.0%')]
        transaction.rollback()

@pytest.mark.integration
def test_repeatVolunteers():
    with mainDB.atomic() as transaction:

        assert list(repeatVolunteers().execute()) == [('Sreynit Khatt', 4), ('Zach Neill', 2)]
        EventParticipant.create(user = 'partont', #Has participated in an event in the Fall term, so we add them to the spring term
                                event = 2,
                                hoursEarned = 1)
        assert list(repeatVolunteers().execute()) == [('Sreynit Khatt', 4), ('Zach Neill', 2), ('Tyler Parton', 2)]
        transaction.rollback()

@pytest.mark.integration
def test_repeatVolunteersPerProgram():
    with mainDB.atomic() as transaction:
        assert list(repeatVolunteersPerProgram().execute()) == [('Zach Neill', 'Hunger Initiatives', 2), ('Sreynit Khatt', 'Adopt-a-Grandparent', 3)]
        EventParticipant.create(user = 'partont', #Has participated in an event in the Fall term, so we add them to the spring term to an event in the hunger initiatives program
                                event = 2,
                                hoursEarned = 1)
        assert list(repeatVolunteersPerProgram().execute()) == [('Zach Neill', 'Hunger Initiatives', 2), ('Tyler Parton', 'Hunger Initiatives', 2),
                                                                ('Sreynit Khatt', 'Adopt-a-Grandparent', 3)]

        transaction.rollback()

@pytest.mark.integration
def test_volunteerMajorAndClass():
    with mainDB.atomic() as transaction:
        assert list(volunteerMajorAndClass(User.major).execute()) == [('Biology', 1), ('Chemistry', 1), ('Computer Science', 2), ('Psychology', 1)]
        assert list(volunteerMajorAndClass(User.classLevel).execute()) == [('Junior', 1), ('Senior', 3), ('Sophomore', 1)]
        assert list(volunteerMajorAndClass(User.classLevel, True).execute()) == [('Sophomore', 1), ('Junior', 1), ('Senior', 3)]
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
                                hoursEarned = 2)
        assert list(volunteerMajorAndClass(User.major).execute()) == [('Agriculture', 1), ('Biology', 1), ('Chemistry', 1), ('Computer Science', 2), ('Psychology', 1)]
        assert list(volunteerMajorAndClass(User.classLevel).execute()) == [('Junior', 1), ('Senior', 3), ('Sophomore', 2)]
        assert list(volunteerMajorAndClass(User.classLevel, True).execute()) == [('Sophomore', 2), ('Junior', 1), ('Senior', 3)]
        transaction.rollback()

@pytest.mark.integration
def test_volunteerHoursByProgram():
    with mainDB.atomic() as transaction:
        assert list(volunteerHoursByProgram().execute()) == [('Adopt-a-Grandparent', 9.0), ('Berea Buddies', 0.0), ('Hunger Initiatives', 11.0)]
        EventParticipant.create(user = 'partont',
                                event = 2,
                                hoursEarned = 1)
        assert list(volunteerHoursByProgram().execute()) == [('Adopt-a-Grandparent', 9.0), ('Berea Buddies', 0.0), ('Hunger Initiatives', 12.0)]
        transaction.rollback()

@pytest.mark.integration
def test_onlyCompletedAllVolunteer():
    with mainDB.atomic() as transaction:
        assert list(onlyCompletedAllVolunteer("2020-2021").execute()) == []
        EventParticipant.create(user = 'partont', #Already participated in an event
                                event = 14, #Added to all volunteer training event
                                hoursEarned = 1)
        assert list(onlyCompletedAllVolunteer("2020-2021").execute()) == []
        User.create(username = 'solijonovam',
                    bnumber = 'B00769465',
                    email = 'solijonovam@berea.edu',
                    phoneNumber = '732-384-3469',
                    firstName = 'Madinabonu',
                    lastName  = 'Solijonova',
                    isStudent = True,
                    major = 'Agriculture',
                    classLevel = 'Sophomore')
        EventParticipant.create(user = 'solijonovam', #Not participated in event
                                event = 14, #Added to all volunteer training event
                                hoursEarned = 1)
        assert list(onlyCompletedAllVolunteer("2020-2021").execute()) == [('solijonovam', 'Madinabonu Solijonova')]
        transaction.rollback()

@pytest.mark.integration
def test_volunteerProgramHours():
    with mainDB.atomic() as transaction:
        assert list(volunteerProgramHours().execute()) == ([('Hunger Initiatives', 'neillz', 4.0),  
                                                            ('Hunger Initiatives', 'khatts', 2.0),
                                                            ('Berea Buddies', 'bryanta', 0.0),
                                                            ('Adopt-a-Grandparent', 'khatts', 9.0),
                                                            ('Hunger Initiatives', 'ayisie', None),
                                                            ('Hunger Initiatives', 'partont', 5.0)])
        EventParticipant.create(user = 'qasema',
                                event = 2,
                                hoursEarned = 1)
        assert list(volunteerProgramHours().execute()) == ([('Hunger Initiatives', 'neillz', 4.0), 
                                                            ('Hunger Initiatives', 'khatts', 2.0), 
                                                            ('Berea Buddies', 'bryanta', 0.0),
                                                            ('Adopt-a-Grandparent', 'khatts', 9.0),
                                                            ('Hunger Initiatives', 'ayisie', None), 
                                                            ('Hunger Initiatives', 'partont', 5.0),
                                                            ('Hunger Initiatives', 'qasema', 1.0)])
        transaction.rollback()

@pytest.mark.integration
def test_totalVolunteerHours():
    with mainDB.atomic() as transaction:
        assert list(totalVolunteerHours().execute()) == [(20.0,)]
        EventParticipant.create(user = 'qasema',
                                event = 2,
                                hoursEarned = 1)
        assert list(totalVolunteerHours().execute()) == [(21.0,)]
        transaction.rollback()

@pytest.mark.integration
def test_getVolunteerProgramEventByTerm():
    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(3)).execute()) == ([])
    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(2)).execute()) == ([('Ebenezer Ayisi', 'ayisie', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
                                                                                  ('Sreynit Khatt', 'khatts', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'),
                                                                                  ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Empty Bowls Spring Event 1'), 
                                                                                  ('Zach Neill', 'neillz', 'Hunger Initiatives', 'Hunger Hurts'),
                                                                                  ('Tyler Parton', 'partont', 'Hunger Initiatives', 'Hunger Hurts')])

    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(4)).execute()) == [('Alex Bryant', 'bryanta', 'Berea Buddies', 'Tutoring'),
                                                                                 ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Adoption 101'),
                                                                                 ('Sreynit Khatt', 'khatts', 'Adopt-a-Grandparent', 'Meet & Greet with Grandparent')]

@pytest.mark.integration
def test_getUniqueVolunteers():
    assert list(getUniqueVolunteers("2021-2022").execute()) == ([('bryanta', 'Alex Bryant', 'B00708826'),
                                                                 ('khatts', 'Sreynit Khatt', 'B00759107')])
 
    assert list(getUniqueVolunteers("2020-2021").execute()) == ([('ayisie', 'Ebenezer Ayisi', 'B00739736'),
                                                                 ('khatts', 'Sreynit Khatt', 'B00759107'),
                                                                 ('neillz', 'Zach Neill', 'B00751864'),
                                                                 ('partont', 'Tyler Parton', 'B00751360')])
import pytest
from app.logic.spreadsheet import *
from app.models.user import User
from app.models.term import Term


@pytest.mark.integration
def test_create_spreadsheet():
    create_spreadsheet("2020-2021")

@pytest.mark.integration
def test_calculateRetentionRate():
    fall_Dict=({'Adopt-a-Grandparent': ['khatts'], 'CELTS-Sponsored Event': [None]})
    spring_dict=({'Hunger Initiatives': ['neillz', 'khatts', 'ayisie', 'neillz', 'partont']})

    assert calculateRetentionRate(fall_Dict,spring_dict) == {'Adopt-a-Grandparent': 0.0, 'CELTS-Sponsored Event': 0.0}
	
@pytest.mark.integration
def test_removeNullParticipants():
	# Test case 1: Dictionary with null participants
    input_dict_1 = {
        'participant1': ['khatts'],
        'participant2': None,
        'participant3': ['neilz'],
        'participant4': None
    }
    expected_result_1 = {
        'participant1': ['khatts'],
        'participant3': ['neilz']
    }
    assert removeNullParticipants(input_dict_1) == expected_result_1

@pytest.mark.integration
def test_termParticipation():
    assert termParticipation('Fall 2020')=={'Adopt-a-Grandparent': ['khatts'], 'CELTS-Sponsored Event': [None]}

@pytest.mark.integration
def test_getRetentionRate():
    assert getRetentionRate("2020-2021") == [('Adopt-a-Grandparent', '0.0%'), ('CELTS-Sponsored Event', '0.0%')]

@pytest.mark.integration
def test_repeatVolunteers():
    assert list(repeatVolunteers().execute()) == [('Sreynit Khatt', 5), ('Zach Neill', 3)]

@pytest.mark.integration
def test_repeatVolunteersPerProgram():
    assert list(repeatVolunteersPerProgram().execute()) == [('Zach Neill', 'Hunger Initiatives', 2), ('Sreynit Khatt', 'Adopt-a-Grandparent', 3)]

@pytest.mark.integration
def test_volunteerMajorAndClass():
    assert list(volunteerMajorAndClass(User.major).execute()) == [('Biology', 1), ('Chemistry', 1), ('Computer Science', 2), ('Psychology', 1)]

@pytest.mark.integration
def test_volunteerHoursByProgram():
    assert list(volunteerHoursByProgram().execute()) == [('Adopt-a-Grandparent', 9.0), ('Berea Buddies', 6.0), ('Hunger Initiatives', 11.0)]

@pytest.mark.integration
def test_onlyCompletedAllVolunteer():
    assert list(onlyCompletedAllVolunteer("2020-2021").execute()) == []

@pytest.mark.integration
def test_volunteerProgramHours():
    assert list(volunteerProgramHours().execute()) == ([('Hunger Initiatives', 'neillz', 4.0),
                                                        ('Hunger Initiatives', 'khatts', 2.0),
                                                        ('Berea Buddies', 'bryanta', 0.0),
                                                        ('Adopt-a-Grandparent', 'khatts', 9.0),
                                                        ('Hunger Initiatives', 'ayisie', None),
                                                        ('Hunger Initiatives', 'partont', 5.0),
                                                        ('Berea Buddies', 'neillz', 3.0),
                                                        ('Berea Buddies', 'khatts', 3.0)])

@pytest.mark.integration
def test_totalVolunteerHours():
    assert list(totalVolunteerHours().execute()) == [(26.0,)]


@pytest.mark.integration
def test_getVolunteerProgramEventByTerm():
    assert list(getVolunteerProgramEventByTerm(Term.get_by_id(3)).execute()) == (
                                [('Sreynit Khatt', 'khatts', 'Berea Buddies', 'Berea Buddies Second Meeting'),
                                 ('Zach Neill', 'neillz', 'Berea Buddies', 'Berea Buddies Second Meeting')])

@pytest.mark.integration
def test_getUniqueVolunteers():
    assert list(getUniqueVolunteers("2021-2022").execute()) == ([('bryanta', 'Alex Bryant', 'B00708826'),
                                                                ('khatts', 'Sreynit Khatt', 'B00759107')])
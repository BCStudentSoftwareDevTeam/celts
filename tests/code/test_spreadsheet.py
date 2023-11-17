import pytest
from app.logic.spreadsheet import create_spreadsheet, getRetentionRate, removeNullParticipants


@pytest.mark.integration
def test_create_spreadsheet():
	create_spreadsheet("2020-2021")

@pytest.mark.integration
def test_calculateRetentionRate():
	pass

@pytest.mark.integration
def test_removeNullParticipants(self):
	# Test case 1: Dictionary with null participants
	input_dict_1 = {
		'participant1': {'name': 'Alice', 'age': 25},
		'participant2': None,
		'participant3': {'name': 'Bob', 'age': 30},
		'participant4': None
	}
	expected_result_1 = {
		'participant1': {'name': 'Alice', 'age': 25},
		'participant3': {'name': 'Bob', 'age': 30}
	}
	self.assertEqual(removeNullParticipants(input_dict_1), expected_result_1)

	# Test case 2: Dictionary with all non-null participants
	input_dict_2 = {
		'participant1': {'name': 'Alice', 'age': 25},
		'participant3': {'name': 'Bob', 'age': 30}
	}
	expected_result_2 = {
		'participant1': {'name': 'Alice', 'age': 25},
		'participant3': {'name': 'Bob', 'age': 30}
	}
	self.assertEqual(removeNullParticipants(input_dict_2), expected_result_2)

	# Test case 3: Empty dictionary
	input_dict_3 = {}
	expected_result_3 = {}
	self.assertEqual(removeNullParticipants(input_dict_3), expected_result_3)


@pytest.mark.integration
def test_termParticipation():
	pass

@pytest.mark.integration
def test_getRetentionRate():
	assert getRetentionRate("2020-2021") == [('Adopt-a-Grandparent', '0.0%'), ('CELTS-Sponsored Event', '0.0%')]

@pytest.mark.integration
def test_repeatVolunteers():
	pass

@pytest.mark.integration
def test_repeatVolunteersPerProgram():
	pass

@pytest.mark.integration
def test_volunteerMajorAndClass():
	pass

@pytest.mark.integration
def test_volunteerHoursByProgram():
	pass

@pytest.mark.integration
def test_onlyCompletedAllVolunteer():
	pass

@pytest.mark.integration
def test_volunteerProgramHours():
	pass

@pytest.mark.integration
def test_totalVolunteerHours():
	pass

@pytest.mark.integration
def test_getVolunteerProgramEventByTerm():
	pass

@pytest.mark.integration
def test_getUniqueVolunteers():
	pass
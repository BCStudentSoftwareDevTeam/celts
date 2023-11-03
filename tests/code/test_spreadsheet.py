import pytest
from app.logic.spreadsheet import create_spreadsheet


@pytest.mark.integration
def test_create_spreadsheet():
	create_spreadsheet("2020-2021")

@pytest.mark.integration
def test_calculateRetentionRate():
	pass

@pytest.mark.integration
def test_removeNullParticipants():
	pass

@pytest.mark.integration
def test_termParticipation():
	pass

@pytest.mark.integration
def test_getRetentionRate():
	pass

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
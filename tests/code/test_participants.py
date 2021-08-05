import pytest
from peewee import DoesNotExist
from app.controllers.admin.addParticipants import *
from app.models.user import User

@pytest.mark.integration
def test_searchVolunteers():
    search = searchVolunteers("Sa")
    assert "Sandesh Lamichhane" in search

@pytest.mark.integration
def test_searchAdmins(): # admins aren't students & shouldn't show in search
    search = searchVolunteers("Br")
    assert "Brian Ramsay" not in search

@pytest.mark.integration
def test_noResults():

    search = searchVolunteers("XXZ")
    assert search == '{}'

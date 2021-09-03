import pytest
from flask import json, jsonify
from app.logic.searchUsers import searchUsers
#from app.controllers.admin.routes import searchVolunteers
from app.models.user import User

# FIXME There are two nearly identical student search functions

#@pytest.mark.integration
#def test_searchVolunteers():
#    search = searchVolunteers("Sa")
#    assert "Sandesh Lamichhane" in search
#
#@pytest.mark.integration
#def test_searchAdmins(): # admins aren't students & shouldn't show in search
#    search = searchVolunteers("Br")
#    assert "Brian Ramsay" not in search
#
#@pytest.mark.integration
#def test_noResults():
#
#    search = searchVolunteers("XXZ")
#    assert search == '{}'
#
@pytest.mark.integration
def test_searchStudents():

    #tests that the search works

    query = 'z'
    searchResults = json.loads(searchUsers(query))
    assert searchResults['Zach Neill (neillz)'] == 'Zach Neill (neillz)'


    #test for last name
    query = 'ramsay'
    searchResults = json.loads(searchUsers(query))
    assert searchResults['Brian Ramsay (ramsayb2)'] == 'Brian Ramsay (ramsayb2)'

    #test with non existing username
    query = 'abc'
    searchResults = json.loads(searchUsers(query))
    assert len(searchResults) == 0

    query = 'its easy as'
    searchResults = json.loads(searchUsers(query))
    assert len(searchResults) == 0

    query = '123'
    searchResults = json.loads(searchUsers(query))
    assert len(searchResults) == 0

    #test with multiple users matching query
    User.get_or_create(username = 'sawconc', firstName = 'Candace', lastName = 'Sawcon', bnumber = '021556782')
    query = 'sa'
    searchResults = json.loads(searchUsers(query))
    assert len(searchResults) == 2
    assert searchResults['Sandesh Lamichhane (lamichhanes2)'] == 'Sandesh Lamichhane (lamichhanes2)'
    assert searchResults['Candace Sawcon (sawconc)'] == 'Candace Sawcon (sawconc)'

    (User.delete().where(User.username == 'sawconc')).execute()

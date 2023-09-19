import pytest
from flask import json, jsonify
from playhouse.shortcuts import model_to_dict

from app.models import mainDB
from app.models.user import User
from app.logic.searchUsers import searchUsers

@pytest.mark.integration
def test_searchUsers():

    #tests that the search works
    searchResults = searchUsers('za')
    assert searchResults['neillz'] == model_to_dict(User.get_by_id('neillz'))

    #test for last name
    searchResults = searchUsers('khat')
    assert searchResults['khatts'] == model_to_dict(User.get_by_id('khatts'))

    #test for first and last name
    searchResults = searchUsers('za nei')
    assert searchResults['neillz'] == model_to_dict(User.get_by_id('neillz'))

    #test with non existing username
    searchResults = searchUsers('abc')
    assert len(searchResults) == 0

    searchResults = searchUsers('its wrong')
    assert len(searchResults) == 0

    #test with multiple users matching query
    with mainDB.atomic() as transaction:
        secondUser = User.create(username = 'sawconc', firstName = 'Candace', lastName = 'Sawcon', bnumber = '021556782', email = 'test@berea.edu', isStudent = True)

        searchResults = searchUsers('sa')
        assert len(searchResults) == 2
        assert searchResults['lamichhanes2'] == model_to_dict(User.get_by_id('lamichhanes2'))
        assert searchResults["sawconc"] == model_to_dict(secondUser)
        assert '(555)555-5555' in searchResults["lamichhanes2"].values()

        transaction.rollback()

@pytest.mark.integration
def test_searchUser_categories():

    # tests that the search categories exclude properly
    searchResults = searchUsers('za', 'instructor')
    assert len(searchResults) == 0
    searchResults = searchUsers('scott', 'admin')
    assert len(searchResults) == 0
    searchResults = searchUsers('sreyn', 'studentstaff')
    assert len(searchResults) == 0
    searchResults = searchUsers('sreyn', 'celtsLinkAdmin')
    assert len(searchResults) == 0

    # tests that the search categories include properly
    searchResults = searchUsers('sco', 'instructor') # faculty
    assert searchResults['heggens'] == model_to_dict(User.get_by_id('heggens'))
    searchResults = searchUsers('bri', 'instructor') # staff
    assert searchResults['ramsayb2'] == model_to_dict(User.get_by_id('ramsayb2'))
    searchResults = searchUsers('brian', 'admin')
    assert searchResults['ramsayb2'] == model_to_dict(User.get_by_id('ramsayb2'))
    searchResults = searchUsers('zach', 'studentstaff')
    assert searchResults['neillz'] == model_to_dict(User.get_by_id('neillz'))
    searchResults = searchUsers('za', 'celtsLinkAdmin')
    assert searchResults['neillz'] == model_to_dict(User.get_by_id('neillz'))

    # Make sure we are getting into these cases for a non-default category
    # test for first and last name
    searchResults = searchUsers('brian r', 'instructor')
    assert searchResults['ramsayb2'] == model_to_dict(User.get_by_id('ramsayb2'))

    # test for last name
    searchResults = searchUsers('ramsa', 'instructor')
    assert searchResults['ramsayb2'] == model_to_dict(User.get_by_id('ramsayb2'))

    # test with non existing username
    searchResults = searchUsers('abc', 'instructor')
    assert len(searchResults) == 0

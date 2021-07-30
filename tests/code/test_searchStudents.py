import pytest
from app.logic.searchStudents import searchVolunteers
from app.models.user import User

@pytest.mark.integration
def test_searchStudents():

    #tests that the search works

    query = 'z'
    searchResults = searchVolunteers(query)
    assert searchResults['Zach Neill (neillz)'] == 'Zach Neill (neillz)'


    #test for last name
    query = 'ramsay'
    searchResults = searchVolunteers(query)
    assert searchResults['Brian Ramsay (ramsayb2)'] == 'Brian Ramsay (ramsayb2)'

    #test with non existing username
    query = 'abc'
    searchResults = searchVolunteers(query)
    assert len(searchResults) == 0

    query = 'its easy as'
    searchResults = searchVolunteers(query)
    assert len(searchResults) == 0

    query = '123'
    searchResults = searchVolunteers(query)
    assert len(searchResults) == 0

    #test with multiple users matching query
    User.get_or_create(username = 'sawconc', firstName = 'Candace', lastName = 'Sawcon', bnumber = '021556782')

    query = 'sa'
    searchResults = searchVolunteers(query)
    print(searchResults)
    assert len(searchResults) == 2
    assert searchResults['Sandesh Lamichhane (lamichhanes2)'] == 'Sandesh Lamichhane (lamichhanes2)'
    assert searchResults['Candace Sawcon (sawconc)'] == 'Candace Sawcon (sawconc)'

    (User.delete().where(User.username == 'sawconc')).execute()

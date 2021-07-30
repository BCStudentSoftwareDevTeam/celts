import pytest
from app.controllers.admin.createEvents import selectFutureTerms
from app.models.term import Term

@pytest.mark.integration
def test_validateListOfTerms():
    currentTermid = 3
    listOfTerms = selectFutureTerms(currentTermid)

    assert 'Fall Break 2021' in listOfTerms and "2024" not in listOfTerms

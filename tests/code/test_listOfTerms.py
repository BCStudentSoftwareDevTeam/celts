import pytest
from app.logic.getFacilitatorsAndTerms import selectFutureTerms
from app.models.term import Term

@pytest.mark.integration
def test_validateListOfTerms():
    currentTermid = 3
    listOfTerms = selectFutureTerms(currentTermid)

    assert Term.get_by_id(3) in listOfTerms and "2024" not in listOfTerms

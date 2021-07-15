import pytest
from app.controllers.admin.routes import createEventPage
from app.models.term import Term

@pytest.mark.integration
def test_validateListOfTerms():
    currentTermid = 3
    termQuery = (Term.select()
                      .where((Term.year <= 2023))
                      .where(Term.id >= currentTermid))

    listTerms = [term.year for term in termQuery]

    assert 2023 in listTerms and 2024 not in listTerms

import pytest
from app.controllers.admin_routes.termManagement import createTerms
from app.models.term import Term
from peewee import DoesNotExist

@pytest.fixture
def setup():
    db_cleanup()
    yield

@pytest.fixture
def cleanup():
    yield
    db_cleanup()

def db_cleanup():
    # data our tests add
    Term.delete().where(Term.termCode.cast('char').contains("2018")).execute()
    Term.delete().where(Term.termCode.cast('char').contains("2021")).execute()
    Term.delete().where(Term.termCode.cast('char').contains("2022")).execute()

    # our demo data puts 2 terms in, let's leave those
    Term.delete().where(Term.termCode.cast('char').contains("2020") & (Term.termCode > 202001)).execute()

@pytest.mark.integration
def test_createTerms(setup, cleanup):
    termsPerYear = 8

    # Initial data sanity
    #################################

    # We should have this term at least
    term = Term.get(Term.termCode == "202000")
    assert "AY 2020-2021"== term.termName
    # We only have 2 to start
    assert 2 == Term.select().where(Term.termCode.cast('char').contains("2020")).count()

    # But not this one or this one
    with pytest.raises(DoesNotExist):
        term = Term.get(Term.termCode == "202100")
    with pytest.raises(DoesNotExist):
        term = Term.get(Term.termCode == "202200")

    # Test createTermsForYear
    #################################

    # This shouldn't break even if they already exist
    createTerms(2020)
    term = Term.get(Term.termCode == "202000")
    assert termsPerYear == Term.select().where(Term.termCode.cast('char').contains("2020")).count()

    # A past year
    createTerms(2018)
    term = Term.get(Term.termCode == "201800")
    assert "AY 2018-2019"== term.termName
    assert True == term.isAcademicYear
    assert termsPerYear == Term.select().where(Term.termCode.cast('char').contains("2018")).count()

    # A future year's terms
    createTerms(2022)
    term = Term.get(Term.termCode == "202200")
    assert "AY 2022-2023"== term.termName

    term = Term.get(Term.termCode == "202201")
    assert "Thanksgiving Break 2022"== term.termName
    assert True == term.isBreak

    term = Term.get(Term.termCode == "202212")
    assert "Spring 2023"== term.termName
    assert False == term.isBreak
    assert termsPerYear == Term.select().where(Term.termCode.cast('char').contains("2022")).count()

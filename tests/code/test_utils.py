import pytest

from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.logic.utils import deep_update, selectSurroundingTerms
from app.logic.userManagement import addCeltsAdmin, removeCeltsAdmin,addCeltsStudentStaff, removeCeltsStudentStaff, changeCurrentTerm, addNextTerm


@pytest.mark.integration
def test_selectSurroundingTerms():
    listOfTerms = selectSurroundingTerms(Term.get_by_id(3))
    assert 9 == len(listOfTerms)

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=0)
    assert [3,4,5,6,7,8,9] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=1)
    assert [2,3,4,5,6,7,8,9] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=-1)
    assert [4,5,6,7,8,9] == [t.id for t in listOfTerms]

@pytest.mark.unit
def test_deepUpdate_empty():
    d1 = {}
    d2 = {"a" : {"key": 7}}
    result = {"a" : {"key": 7}}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    d1 = {"a" : {"key": 7}}
    d2 = {}
    result = {"a" : {"key": 7}}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    d1 = {"a" : {"key": 7}}
    d2 = None
    result = {"a" : {"key": 7}}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    # since there is no reference parameter to update, we can only check the return value
    d1 = None
    d2 = {"b": {"alpha" : 17}}
    result = {"b": {"alpha" : 17}}

    return_val = deep_update(d1, d2)
    assert result == return_val


@pytest.mark.unit
def test_deepUpdate():
    d1 = {"a" : 1}
    d2 = {"b": 2, "a": 3}
    result = {"a": 3, "b": 2}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    d1 = {"a" : {"key": 7}}
    d2 = {"b": 2, "a": 3}
    result = {"a": 3, "b": 2}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    d1 = {"a" : 3}
    d2 = {"b": 2, "a": {"key": 7}}
    result = {"a": {"key": 7}, "b": 2}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    d1 = {"a" : {"key": 8}}
    d2 = {"b": 2, "a": {"key": 7}}
    result = {"a": {"key": 7}, "b": 2}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

    d1 = {"a" : {"key": 8}}
    d2 = {"b": 2, "a": {"newkey": 12}}
    result = {"a": {"key": 8, "newkey": 12}, "b": 2}

    return_val = deep_update(d1, d2)
    assert result == d1
    assert result == return_val

def test_changeCurrentTerm():
    # test via g.current_term
    oldTerm = g.current_term
    changeCurrentTerm(2)
    assert g.current_term == 2
    assert not oldTerm

    # test via isCurrentTerm
    oldTerm2 = g.current_term
    newTerm = changeCurrentTerm(1)
    assert newTerm.isCurrentTerm
    assert not oldTerm2 == g.current_term
    assert not oldTerm2.isCurrentTerm

    # reset data back to before test
    changeCurrentTerm(oldTerm)

def test_invalidTermInputs():
    with pytest.raises(DoesNotExist):
        changeCurrentTerm(100)
    with pytest.raises(DoesNotExist):
        changeCurrentTerm("womp")

@pytest.mark.integration
def test_addNextTerm():
    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Summer 2022",year=2022, academicYear= "2021-2022", isSummer=True,isCurrentTerm=True)
        testTerm.save()

        addNextTerm()

        # for the first test,  make sure we're using the db properly
        terms = list(Term.select().order_by(Term.id))
        newTerm = terms[-1]
        assert newTerm.description == "Fall 2022"
        assert newTerm.year == 2022
        assert newTerm.academicYear == "2022-2023"
        assert not newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()


    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Fall 2029",year=2029, academicYear= "2029-2030", isSummer=False,isCurrentTerm=False)
        testTerm.save()

        newTerm = addNextTerm()
        assert newTerm.description == "Spring 2030"
        assert newTerm.year == 2030
        assert newTerm.academicYear == "2029-2030"
        assert not newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()


    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Spring 2022",year=2022, academicYear= "2021-2022", isSummer=False,isCurrentTerm=False)
        testTerm.save()

        newTerm = addNextTerm()
        assert newTerm.description == "Summer 2022"
        assert newTerm.year == 2022
        assert newTerm.academicYear == "2021-2022"
        assert newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()

@pytest.mark.integration
def test_getStartofCurrentAcademicYear():
    with mainDB.atomic() as transaction:
        # Case1: current term is Fall 2020
        currentTerm = Term.get_by_id(1)
        fallTerm = currentTerm.academicYearStartingTerm
        assert fallTerm.year == 2020
        assert fallTerm.description == "Fall 2020"
        assert fallTerm.academicYear == "2020-2021"

        # Case2: current term is Spring 2021
        currentTerm = Term.get_by_id(2)
        fallTerm = currentTerm.academicYearStartingTerm
        assert fallTerm.year == 2020
        assert fallTerm.description == "Fall 2020"
        assert fallTerm.academicYear == "2020-2021"

        # Case3: current term is Summer 2021
        currentTerm = Term.get_by_id(4)
        fallTerm = currentTerm.academicYearStartingTerm

        assert fallTerm.year == 2020
        assert fallTerm.description == "Fall 2020"
        assert fallTerm.academicYear == "2020-2021"

        transaction.rollback()

@pytest.mark.integration
def test_isFutureTerm():
    with mainDB.atomic() as transaction:
        dbCurrentTerm = Term.select().where(Term.isCurrentTerm == True).get()
        dbCurrentTerm.isCurrentTerm = False
        dbCurrentTerm.save()
        testCurrentTerm = Term.create(description = "Summer 1900",
                                    year = 1900,
                                    academicYear = "1899-1900",
                                    isSummer = True,
                                    isCurrentTerm = True)
        sameYearFutureTerm = Term.create(description = "Fall 1900",
                                    year = 1900,
                                    academicYear = "1900-1901",
                                    isSummer = False,
                                    isCurrentTerm = False)
        sameYearPastTerm = Term.create(description = "Spring 1900",
                                    year = 1900,
                                    academicYear = "1899-1900",
                                    isSummer = False,
                                    isCurrentTerm = False)
        futureYearTerm = Term.create(description = "Fall 1901",
                                    year = 1901,
                                    academicYear = "1901-1902",
                                    isSummer = False,
                                    isCurrentTerm = False)
        pastYearTerm = Term.create(description = "Spring 1899",
                                    year = 1899,
                                    academicYear = "1899-1900",
                                    isSummer = False,
                                    isCurrentTerm = False)
        # future term this year
        assert sameYearFutureTerm.isFutureTerm == True
        # future term in future year
        assert futureYearTerm.isFutureTerm == True
        # past term this year
        assert sameYearPastTerm.isFutureTerm == False
        # past term previous year
        assert pastYearTerm.isFutureTerm == False
        # current term
        assert testCurrentTerm.isFutureTerm == False
        transaction.rollback()

import pytest
from app.logic.userManagement import addCeltsAdmin, removeCeltsAdmin,addCeltsStudentStaff, removeCeltsStudentStaff, changeCurrentTerm, addNextTerm
from app.models.user import User
from app.models.term import Term
from app.logic.utils import deep_update, selectSurroundingTerms

@pytest.mark.integration
def test_selectSurroundingTerms():
    listOfTerms = selectSurroundingTerms(Term.get_by_id(3))
    assert [1,2,3,4,5] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=0)
    assert [3,4,5] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=1)
    assert [2,3,4,5] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=-1)
    assert [4,5] == [t.id for t in listOfTerms]

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
    newTerm = Term.create(description="Fall 2022",year=2022, academicYear= "2022-2023",isBreak=False, isSummer=False,isCurrentTerm=False)
    newTerm.save()

    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = newTerm
    addNextTerm()
    terms = list(Term.select().order_by(Term.id))
    newlyAddedTerm = terms[-1]
    assert newlyAddedTerm.description == "Spring 2023"

    query = Term.get(Term.id == lastCreatedTerm)
    query.delete_instance()
    query = Term.get(Term.id == newlyAddedTerm)
    query.delete_instance()

    newTerm = Term.create(description="Fall 2029",year=2029, academicYear= "2029-2030",isBreak=False, isSummer=False,isCurrentTerm=False)
    newTerm.save()

    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = terms[-1]
    addNextTerm()
    terms = list(Term.select().order_by(Term.id))
    newlyAddedTerm = terms[-1]
    assert newlyAddedTerm.description == "Spring 2030"

    query = Term.get(Term.id == lastCreatedTerm)
    query.delete_instance()
    query = Term.get(Term.id == newlyAddedTerm)
    query.delete_instance()

    newTerm = Term.create(description="Spring 2022",year=2022, academicYear= "2021-2022",isBreak=False, isSummer=False,isCurrentTerm=False)
    newTerm.save()

    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = terms[-1]
    addNextTerm()
    terms = list(Term.select().order_by(Term.id))
    newlyAddedTerm = terms[-1]
    assert newlyAddedTerm.description == "Summer 2022"

    query = Term.get(Term.id == lastCreatedTerm)
    query.delete_instance()
    query = Term.get(Term.id == newlyAddedTerm)
    query.delete_instance()

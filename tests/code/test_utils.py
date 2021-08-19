import pytest

from app.models.term import Term
from app.logic.utils import deep_update
from app.logic.getFacilitatorsAndTerms import selectFutureTerms

@pytest.mark.integration
def test_validateListOfTerms():
    currentTermid = 3
    listOfTerms = selectFutureTerms(currentTermid)

    assert Term.get_by_id(3) in listOfTerms and "2024" not in listOfTerms

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

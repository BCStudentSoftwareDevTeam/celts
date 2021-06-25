import pytest

from app.logic.utils import deep_update

@pytest.mark.integration
def test_deepUpdate():
    d1 = {"a" : 1}
    d2 = {"b": 2, "a": 3}
    result = {"a": 3, "b": 2}

    deep_update(d1, d2)
    assert result == d1

    d1 = {"a" : {"key": 7}}
    d2 = {"b": 2, "a": 3}
    result = {"a": 3, "b": 2}

    deep_update(d1, d2)
    assert result == d1

    d1 = {"a" : 3}
    d2 = {"b": 2, "a": {"key": 7}}
    result = {"a": {"key": 7}, "b": 2}

    deep_update(d1, d2)
    assert result == d1

    d1 = {"a" : {"key": 8}}
    d2 = {"b": 2, "a": {"key": 7}}
    result = {"a": {"key": 7}, "b": 2}

    deep_update(d1, d2)
    assert result == d1

    d1 = {"a" : {"key": 8}}
    d2 = {"b": 2, "a": {"newkey": 12}}
    result = {"a": {"key": 8, "newkey": 12}, "b": 2}

    deep_update(d1, d2)
    assert result == d1

    d1 = {"a" : {"key": 8}}
    d2 = {}
    result = {"a" : {"key": 8}}

    deep_update(d1, d2)
    assert result == d1


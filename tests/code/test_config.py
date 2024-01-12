import pytest
import os

from app.logic.config import load_config_files, update_config_from_yaml, deep_update
from app.__init__ import app

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

@pytest.mark.integration
def test_update_config_from_yaml():
    """Testing to make sure setting the config from YML files works properly"""
    update_config_from_yaml(app, "default.yml")
    assert(app.config["test_entry"] == "Default")
    # test the value set by default yaml
    assert(app.config["MAIL_ENABLED"] == True)
    # test the value set by default yaml

    update_config_from_yaml(app, f"{app.env}.yml")
    # test that something that is in default and in testing is updated after the override
    assert(app.config["test_entry"] == "Testing")
    # test that something that is in default but not in testing is still there after the override
    assert(app.config["MAIL_ENABLED"] == True)

    # NOTE: cannot test load_config_file because everyone has independent local-override which could break tests

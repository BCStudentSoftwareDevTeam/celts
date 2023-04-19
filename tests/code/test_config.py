import pytest
import os

from flask.helpers import get_env

from app.logic.config import load_config_files, update_config_from_yaml
from app.__init__ import app

@pytest.mark.integration
def test_update_config_from_yaml():
    """Testing to make sure setting the config from YML files works properly"""
    update_config_from_yaml(app, "default.yml")
    assert(app.config["test_entry"] == "Default")
    # test the value set by default yaml
    assert(app.config["MAIL_ENABLED"] == True)
    # test the value set by default yaml

    update_config_from_yaml(app, f"{get_env()}.yml")
    # test that something that is in default and in testing is updated after the override
    assert(app.config["test_entry"] == "Testing")
    # test that something that is in default but not in testing is still there after the override
    assert(app.config["MAIL_ENABLED"] == True)

    # NOTE: cannot test load_config_file because everyone has independent local-override which could break tests

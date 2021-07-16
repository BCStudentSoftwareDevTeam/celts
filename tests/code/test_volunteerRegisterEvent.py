import pytest
from app.controllers.main.volunteerRegisterEvents import volunteerRegister
from app.controllers.admin import admin_bp


@pytest.mark.integration
def test_volunteerRegister():
    registration = volunteerRegister()
    assert registration == "It didn't work"

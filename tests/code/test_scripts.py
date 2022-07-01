import pytest
from app.scripts.sendEventReminderEmails import checkForEvents

@pytest.mark.integration
def test_checkForEvents():
    checkForEvents()

import pytest
from pytest import raises
from celery.exceptions import Retry
from unittest.mock import patch
from datetime import datetime, timedelta
from app.models.event import Event

from app.logic.tasks import sendEmailTask


@pytest.mark.integration
def test_success():
    raw_form_data = {"templateIdentifier": "Test",
        "programID":"1",
        "eventID":"1",
        "recipientsCategory": "Interested"}

    url_domain = "1234"
    event = Event.get_by_id(raw_form_data["eventID"])
    arrivalDate = datetime.utcnow() + timedelta(seconds=5) - timedelta(hours=4)
    print("\n arrivalDate", arrivalDate, "\n")

    assert sendEmailTask.apply_async(args=[raw_form_data, url_domain], countdown=5).get(timeout=30) == {"status": True}

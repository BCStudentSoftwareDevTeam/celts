import pytest
from peewee import DoesNotExist

from app.controllers.events.view_transcript import ViewTranscript

@pytest.mark.integration
def test_viewTranscript():
    # No program is given
    transcript = ViewTranscript()
    assert transcript

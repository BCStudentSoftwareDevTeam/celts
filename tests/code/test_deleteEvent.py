import pytest
from app.controllers.admin.deleteEvent import deleteEvent
from app.models.event import Event

@pytest.mark.integration
def test_deleteEvent():
    program = 1
    eventId = 2
    deletingEvent = deleteEvent(program, eventId)

    assert Event.get_or_none(Event.id == eventId) is None

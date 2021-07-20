import pytest
from peewee import DoesNotExist

from app.logic.events import getEvents
from app.models.interest import Interest

@pytest.mark.integration
def test_getEventsNoProgram():
    # No program is given, get all events
    events = getEvents()


    assert len(events) > 0


    assert events[0].description == "Empty Bowls Spring 2021"
    assert events[1].description == "This is a Test"
    assert events[2].description == "Adopt A Grandparent"

@pytest.mark.integration
def test_getEventsWithProgram():
    # Single program
    events = getEvents(program_id=2)


    assert len(events) > 0


    assert events[0].description == "Berea Buddies First Meetup"

@pytest.mark.integration
def test_getEventsInvalidProgram():
    # Invalid program
    with pytest.raises(DoesNotExist):
        getEvents(program_id= "asdf")

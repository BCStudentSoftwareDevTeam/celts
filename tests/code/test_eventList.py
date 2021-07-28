import pytest
from app.logic.events import groupEventsByCategory, groupEventsByProgram
from peewee import DoesNotExist
from app.models.program import Program
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.models.term import Term

@pytest.mark.integration
def test_termDoesNotExist():
    with pytest.raises(DoesNotExist):
        groupedEvents = groupEventsByCategory(7)
        groupedEvents2 = groupEventsByCategory("khatts")

@pytest.mark.integration
def test_groupEventsByProgram():
    studentLedEvents = (Event.select(Event, Program)
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == 1))
    groupedEvents = groupEventsByProgram(studentLedEvents)
    assert groupedEvents == {'Empty Bowls': ['Empty Bowls Spring 2021', 'Berea Buddies Training']}

@pytest.mark.integration
def test_correctQuerying():

    assert groupEventsByCategory(3)

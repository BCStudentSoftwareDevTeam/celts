import pytest
from app.logic.events import groupingEvents, groupEventsByProgram
from peewee import DoesNotExist
from app.models.program import Program
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.models.term import Term

@pytest.mark.integration
def test_termDoesNotExist():
    with pytest.raises(DoesNotExist):
        assert 'Fall 2010' in groupingEvents(100)
        assert 'Spring 2018' in groupingEvents(4)

@pytest.mark.integration
def test_groupEventsByProgram():
    studentLedEvents = (Event.select(Event, Program)
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == 3))
    assert groupEventsByProgram(studentLedEvents)

@pytest.mark.integration
def test_correctQuerying():
    # assert 'Spring A 2021' in groupingEvents(1)
    # assert [] in groupingEvents(2)
    # assert [Program.get_by_id(1), Program.get_by_id(2), Program.get_by_id(3)] in groupingEvents(3)

    assert groupingEvents(3)

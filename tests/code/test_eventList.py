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
    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == 1))
    groupedEvents = groupEventsByProgram(studentLedEvents)
    assert groupedEvents == {Program.get_by_id(1): [Event.get_by_id(1), Event.get_by_id(2)]}

@pytest.mark.integration
def test_groupEventsByCategory():
    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == 1))
    groupedeventsByCategory = groupEventsByCategory(1)

    assert groupedeventsByCategory

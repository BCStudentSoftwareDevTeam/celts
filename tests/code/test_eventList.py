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

    with pytest.raises(DoesNotExist):
        groupedEvents2 = groupEventsByCategory("khatts")

    with pytest.raises(DoesNotExist):
        groupedEvents3 = groupEventsByCategory("")

@pytest.mark.integration
def test_groupEventsByProgram():
    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == 1))
    assert groupEventsByProgram(studentLedEvents) == {Program.get_by_id(1): [Event.get_by_id(1), Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]}

    trainingEvents = (Event.select(Event, Program.id.alias("program_id"))
                           .join(ProgramEvent)
                           .join(Program)
                           .where(Event.isTraining,
                                  Event.term == 1))
    assert groupEventsByProgram(trainingEvents) == {Program.get_by_id(1): [Event.get_by_id(1) , Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]}

    bonnerScholarsEvents = (Event.select(Event, Program.id.alias("program_id"))
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == 1))
    assert groupEventsByProgram(bonnerScholarsEvents) == {}

    oneTimeEvents = (Event.select(Event, Program.id.alias("program_id"))
                          .join(ProgramEvent)
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False,
                                 Event.term == 1))
    assert groupEventsByProgram(oneTimeEvents) == {}


@pytest.mark.integration
def test_groupEventsByCategory():
    groupedEventsByCategory = groupEventsByCategory(1)
    assert groupedEventsByCategory == {"Student Led Events" : {Program.get_by_id(1): [Event.get_by_id(1), Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]},
                         "Trainings" : {Program.get_by_id(1): [Event.get_by_id(1) , Event.get_by_id(2)] , Program.get_by_id(2): [Event.get_by_id(4)]} ,
                         "Bonner Scholars" : {} ,
                         "One Time Events" : {} }

    assert groupedEventsByCategory

import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.event import Event
from app.models.event import Term
from app.logic.events import getStudentLedEvents,  getTrainingEvents, getBonnerEvents, getNonProgramEvents

@pytest.mark.integration
@pytest.fixture
def training_event():
        testEvent = Event.create(name = "Test Student Lead",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)

        testProgramEvent = ProgramEvent.create(program = 5, event = testEvent)

        yield testEvent

        testEvent.delete_instance(testProgramEvent)

@pytest.mark.integration
def test_studentled_event(training_event):
        testProgramEvent = getStudentLedEvents(3)
        assert testProgramEvent

@pytest.mark.integration
def test_training_event(training_event):

        newTerm= Term.create(
            description= "Fall 2025",
            year= 2025,
            academicYear= 2024-2025,
            isSummer= 0,
            isCurrentTerm=0)

        testProgramEvent = getTrainingEvents(3)
        testProgramEvent2 = getTrainingEvents(newTerm)

        assert testProgramEvent not in testProgramEvent2

        newTerm.delete_instance()

@pytest.mark.integration
def test_bonner_event(training_event):
    testProgramEvent = getBonnerEvents(3)
    assert testProgramEvent

@pytest.mark.integration
def test_nonProgram_event(training_event):
    testProgramEvent = getNonProgramEvents(6)

    assert testProgramEvent

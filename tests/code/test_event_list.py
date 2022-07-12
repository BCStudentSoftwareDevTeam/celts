import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.event import Event
from app.models.event import Term
from app.logic.events import getStudentLedEvents,  getTrainingEvents, getBonnerEvents, getNonProgramEvents

@pytest.mark.integration
@pytest.fixture
# pytest fixture: used to setup the test data that can be resused in all of the
# tests.
def training_events():
    testEvent = Event.create(name = "Test Student Lead",
                            term = 2,
                            description = "event for testing",
                            timeStart = "18:00:00",
                            timeEnd = "21:00:00",
                            location = "basement",
                            startDate = 2021-12-12,
                            endDate = 2021-12-13)

    testProgramEvent = ProgramEvent.create(program = 2 , event = testEvent)
    yield testProgramEvent

    testEvent.delete_instance(testProgramEvent)

@pytest.mark.integration
def test_studentled_events(training_events):
    studentLed = training_events
    allStudentLedProgram = {studentLed.program: [studentLed.event]}

    assert allStudentLedProgram == getStudentLedEvents(2)


# @pytest.mark.integration
# def test_training_events(training_events):
#
#
# @pytest.mark.integration
# def test_bonner_events(training_events):
#
#
#
# @pytest.mark.integration
# def test_nonProgram_events(training_events):
#

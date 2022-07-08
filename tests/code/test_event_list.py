import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.event import Event
from app.models.event import Term
from app.logic.events import getStudentLedEvents,  getTrainingEvents, getBonnerEvents, getNonProgramEvents

# @pytest.mark.integration
# @pytest.fixture
# def training_events():
#     # testEvent = Event.create(name = "Test Student Lead",
#     #                         term = 3,
#     #                         description = "event for testing",
#     #                         timeStart = "18:00:00",
#     #                         timeEnd = "21:00:00",
#     #                         location = "basement",
#     #                         startDate = 2021-12-12,
#     #                         endDate = 2021-12-13)
#
#     testProgramEvent = ProgramEvent.create(program = 5, event = 1)
#     return testProgramEvent
#     # yield testProgramEvent
#     #
#     #testEvent.delete_instance(testProgramEvent)
#
# @pytest.mark.integration
# def test_studentled_events(training_events):
#
#
#
# @pytest.mark.integration
# def test_training_events(training_events):
#     testProgramEvent = getTrainingEvents(3)
#
#     assert testProgramEvent
#
# @pytest.mark.integration
# def test_bonner_events(training_events):
#     testProgramEvent = getBonnerEvents(3)
#
#     assert testProgramEvent
#
# @pytest.mark.integration
# def test_nonProgram_events(training_events):
#     testProgramEvent = getNonProgramEvents(6)
#
#     assert testProgramEvent

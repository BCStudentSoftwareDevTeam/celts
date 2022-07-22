import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.event import Event
from app.models.event import Term
from app.logic.events import getStudentLedEvents,  getTrainingEvents, getBonnerEvents, getOtherEvents

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
                            isTraining = True,
                            startDate = "2021-12-12",
                            endDate = "2021-12-13")

    testProgramEvent = ProgramEvent.create(program = 2 , event = testEvent)

    yield testProgramEvent
    testEvent.delete_instance(testProgramEvent)

@pytest.mark.integration
@pytest.fixture
def special_bonner():
    bonnerEvent = Event.create(name = "Test For Bonner",
                            term = 2,
                            description = "Special event test for Bonner",
                            timeStart = "19:00:00",
                            timeEnd = "22:00:00",
                            location = "moon",
                            startDate = "2021-12-12",
                            endDate = "2021-12-13")

    specialForBonner = ProgramEvent.create(program = 5, event = bonnerEvent)

    yield specialForBonner
    bonnerEvent.delete_instance(specialForBonner)

@pytest.mark.integration
@pytest.fixture
def special_otherEvents():
        nonProgramEvent = Event.create(name = "Test for nonProgram",
                                term = 4,
                                description = "Special event test for nonProgram",
                                timeStart = "19:00:00",
                                timeEnd = "22:00:00",
                                location = "moon",
                                isTraining = False,
                                startDate = "2021-12-12",
                                endDate = "2021-12-13")

        yield nonProgramEvent
        nonProgramEvent.delete_instance()

@pytest.mark.integration
def test_studentled_events(training_events):
    studentLed = training_events
    allStudentLedProgram = {studentLed.program: [studentLed.event]}

    assert allStudentLedProgram == getStudentLedEvents(2)

@pytest.mark.integration
def test_training_events(training_events):
    training = training_events
    allTrainingPrograms = [Event.get_by_id(1), training.event]

    assert allTrainingPrograms == getTrainingEvents(2)

@pytest.mark.integration
def test_bonner_events(special_bonner):
    bonner = special_bonner
    allBonnerProgram = [bonner.event]

    assert allBonnerProgram == getBonnerEvents(2)

@pytest.mark.integration
def test_getOtherEvents(special_otherEvents):
    otherEvent = special_otherEvents
    otherEvents = [Event.get_by_id(7), Event.get_by_id(11), otherEvent]

    assert otherEvents == getOtherEvents(4)

import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.event import Event
from app.models.event import Term
from app.logic.events import getStudentLedProgram,  getTrainingProgram, getBonnerProgram, getNonProgramEvents

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

        testProgramEvent = ProgramEvent.create(program = 3, event = testEvent)

        yield testEvent

        testEvent.delete_instance(testProgramEvent)

@pytest.mark.integration
def test_studentled_event(training_event):
        testProgramEvent = getStudentLedProgram(3)
        assert testProgramEvent
        print(testProgramEvent)


@pytest.mark.integration
def test_training_event(training_event):

        newTerm= Term.create(
            description= "Fall 2025",
            year= 2025,
            academicYear= 2024-2025,
            isSummer= 0,
            isCurrentTerm=0)

        testProgramEvent = getTrainingProgram(3)
        testProgramEvent2 = getTrainingProgram(2)
        testProgramEvent3 = getTrainingProgram(newTerm)
        newTerm.delete_instance()


# @pytest.mark.integration
# def test_bonner_event(training_event):


# @pytest.mark.integration
# def test_oneTime_event(training_event):

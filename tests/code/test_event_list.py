import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.event import Event
from app.models.event import Term
from app.logic.events import getStudentLedProgram,  getTrainingProgram, getBonnerProgram, getOneTimeEvents
'''
@pytest.mark.integration
def test_event_list():
    with mainDB.atomic() as transaction:
        Studentled = Event.create(name = "Test Student Lead",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        studentProgramEvent = ProgramEvent.create(program = 2, event = Studentled)

        training = Event.create(name = "Test Training Program",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                isTraining = 1,
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        trainingProgramEvent = ProgramEvent.create(program = 2, event = training)

        bonner = Event.create(name = "Test Bonner Program",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        bonnerProgramEvent = ProgramEvent.create(program = 5, event = bonner)

        oneTime = Event.create(name = "Test One Time",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        oneTimeProgramEvent = ProgramEvent.create(program = 6, event = oneTime)

        newTerm= Term.create(
            description= "Fall 2025",
            year= 2025,
            academicYear= 2024-2025,
            isSummer= 0,
            isCurrentTerm=0)
        studentledProgram = getStudentLedProgram(3)
        assert studentledProgram
        studentledRes = []
        for program, events in studentledProgram.items():
            for event in events:
                studentledRes.append(event.name)
        assert "Test Student Lead" in studentledRes

        trainingProgram = getTrainingProgram(3)
        trainingProgram2 = getTrainingProgram(2)
        trainingProgram3 = getTrainingProgram(newTerm)
        newTerm.delete_instance()

        assert trainingProgram
        assert training in trainingProgram
        assert Studentled not in studentledProgram
        assert training not in trainingProgram2
        assert trainingProgram3 == []

        bonnerProgram = getBonnerProgram(3)
        assert bonnerProgram
        assert bonner in bonnerProgram
        assert Studentled not in bonnerProgram

        oneTimeEvents = getOneTimeEvents(3)
        assert oneTimeEvents
        assert oneTime in oneTimeEvents
        assert Studentled not in oneTimeEvents

        transaction.rollback()
'''
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

        testProgramEvent = ProgramEvent.create(program = 2, event = testEvent)

        yield testEvent

        testEvent.delete_instance(testProgramEvent)

@pytest.mark.integration
def test_studentled_event(training_event):
        testProgramEvent = getStudentLedProgram(3)
        assert testProgramEvent
        print(testProgramEvent)

        studentledRes = []

        for program, events in testProgramEvent.items():
            for event in events:
                studentledRes.append(event.name)

        assert "Test Student Lead" in studentledRes
        print(studentledRes)
'''
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


@pytest.mark.integration
def test_bonner_event(training_event):
        testProgramEvent = getBonnerProgram(3)
        assert testProgramEvent
        assert testEvent in testProgramEvent
        #assert Studentled not in bonnerProgram

@pytest.mark.integration
def test_oneTime_event(training_event):
        oneTimeEvents = getOneTimeEvents(3)
        assert oneTimeEvents
        assert oneTime in oneTimeEvents
        assert Studentled not in oneTimeEvents

'''

import pytest
from peewee import DoesNotExist
from app.models import mainDB
from app.models.programEvent import ProgramEvent
from app.models.event import Event
from app.logic.events import getStudentLeadProgram,  getTrainingProgram, getBonnerProgram, getOneTimeEvents

@pytest.mark.integration
def test_event_list():
    with mainDB.atomic() as transaction:
        studentLead = Event.create(eventName = "Test Student Lead",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                isRecurring = 0,
                                isRsvpRequired = 0,
                                isTraining = 0,
                                isService = 0,
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        studentProgramEvent = ProgramEvent.create(program = 1, event = studentLead)

        training = Event.create(eventName = "Test Training Program",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                isRecurring = 0,
                                isRsvpRequired = 0,
                                isTraining = 1,
                                isService = 0,
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        trainingProgramEvent = ProgramEvent.create(program = 2, event = training)

        bonner = Event.create(eventName = "Test Bonner Program",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                isRecurring = 0,
                                isRsvpRequired = 0,
                                isTraining = 0,
                                isService = 0,
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        bonnerProgramEvent = ProgramEvent.create(program = 5, event = bonner)


        oneTime = Event.create(eventName = "Test One Time",
                                term = 3,
                                description = "event for testing",
                                timeStart = "18:00:00",
                                timeEnd = "21:00:00",
                                location = "basement",
                                isRecurring = 0,
                                isRsvpRequired = 0,
                                isTraining = 0,
                                isService = 0,
                                startDate = 2021-12-12,
                                endDate = 2021-12-13)
        oneTimeProgramEvent = ProgramEvent.create(program = 6, event = oneTime)

        studentLeadProgram = getStudentLeadProgram(3)
        studentLeadProgram2 = getStudentLeadProgram(2)
        trainingProgram = getTrainingProgram(3)
        trainingProgram2 = getTrainingProgram(2)
        bonnerProgram = getBonnerProgram(3)
        oneTimeEvents = getOneTimeEvents(3)

        assert studentLeadProgram
        assert True in [program.programName == "Empty Bowls" for program,events in studentLeadProgram.items()]
        assert [True] in [[event.eventName == "Test Student Lead" for event in events] for program, events in studentLeadProgram.items()]
        assert [True] not in [[event.eventName == "Test Training Program" for event in events] for program, events in studentLeadProgram.items()]

        assert trainingProgram
        assert True in [event.eventName == "Test Training Program" for event in trainingProgram]
        assert True not in [event.eventName == "Test Student Lead" for event in trainingProgram]
        assert True not in [event.eventName == "Test Training Program" for event in trainingProgram2]

        assert bonnerProgram
        assert True in [event.eventName == "Test Bonner Program" for event in bonnerProgram]
        assert True not in [event.eventName == "Test Training Program" for event in bonnerProgram]

        assert oneTimeEvents
        assert True in [event.eventName == "Test One Time" for event in oneTimeEvents]
        assert True not in [event.eventName == "Test Training Program" for event in oneTimeEvents]

        transaction.rollback()

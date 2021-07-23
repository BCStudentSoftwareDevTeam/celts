import pytest
from app.logic.programSelect import programTemplates


@pytest.mark.integration
def test_programTemplates():

    createEventsDict = {}
    allVolTrainingEvent = programTemplates("allVolunteerTraining", createEventsDict )
    assert allVolTrainingEvent

    studentLedProgramsTrainingEvent = programTemplates("studentLedProgramsTraining", createEventsDict)
    assert studentLedProgramsTrainingEvent

    # Program in Database
    generalCreateEvents = programTemplates("Food Drive", createEventsDict )
    assert generalCreateEvents

    # Program not in database and not "allVolunteerTraining" nor "studentLedProgramsTraining"
    generalCreateEvents1 = programTemplates("notaprogram", createEventsDict )
    assert not generalCreateEvents1

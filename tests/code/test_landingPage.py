import pytest, os
from flask import g
from app import app
from peewee import DoesNotExist, OperationalError, IntegrityError

from app.models import mainDB
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.term import Term

from app.logic.landingPage import getManagerProgramDict, getActiveEventTab

@pytest.mark.integration
def test_activeEventTab():
    with mainDB.atomic() as transaction:

        studentLed = Program.create(programName = "SL",
                                          isStudentLed = True,
                                          isBonnerScholars = False,
                                          contactEmail = "test@email",
                                          contactName = "testName")
        assert getActiveEventTab(studentLed.id) == "studentLedEvents"

        bonnerScholars1 = Program.create(programName = "BS1",
                                           isStudentLed = False,
                                           isBonnerScholars = True,
                                           contactEmail = "test@email",
                                           contactName = "testName")
        assert getActiveEventTab(bonnerScholars1.id) == "bonnerScholarsEvents"

        bonnerScholars2 = Program.create(programName = "BS2",
                                           isStudentLed = True,
                                           isBonnerScholars = True,
                                           contactEmail = "test@email",
                                           contactName = "testName")
        assert getActiveEventTab(bonnerScholars2.id) == "bonnerScholarsEvents"

        other = Program.create(programName = "OP",
                                           isStudentLed = False,
                                           isBonnerScholars = False,
                                           contactEmail = "test@email",
                                           contactName = "testName")
        assert getActiveEventTab(other.id) == "otherEvents"

        transaction.rollback()

@pytest.mark.integration
def test_managerProgramDict():
    with mainDB.atomic() as transaction:

        dict = getManagerProgramDict()
        assert os.path.join('static', 'images/landingPage/Hunger Initiatives.jpg') in dict[Program.get(Program.programName == "Hunger Initiatives")]["image"]

        fakeProgram = Program.create(programName = "Fake Program",
                                          isStudentLed = False,
                                          isBonnerScholars = False,
                                          contactEmail = "",
                                          contactName = "")

        dict = getManagerProgramDict()
        assert fakeProgram in dict
        assert os.path.join('static', 'images/logos/celts_symbol.png') in dict[fakeProgram]["image"]

        transaction.rollback()

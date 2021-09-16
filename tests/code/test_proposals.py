import pytest
from peewee import IntegrityError, DoesNotExist

from app.models.program import Program
from app.models.user import User
from app.logic.getSLInstructorTableData import getProposalData
from app.controllers.admin.changeSLAction import withdrawCourse

@pytest.mark.integration
def test_isCorrectData():
    courseDict = getProposalData('ramsayb2')
    assert 'Databases' in courseDict
    assert 'Brian Ramsay' in courseDict['Databases']['faculty']
    assert ['Brian Ramsay', 'Zach Neill'] == courseDict['Spanish Help']['faculty']
    assert 'Approved' in courseDict['Spanish Help']['status']
    assert 'Spring A 2021' in courseDict['Spanish Help']['term'].description
    assert not 'Internship' in courseDict

import pytest
from flask import g

from app import app
from app.logic.graduationManagement import setGraduatedStatus, getGraduationManagementUsers, updateHideGraduatedStudents
from app.logic.utils import getHideGraduatedStudentsWhereClause 
from app.models import mainDB
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models.bonnerCohort import BonnerCohort
from app.models.celtsLabor import CeltsLabor
from app.models.courseParticipant import CourseParticipant
from app.models.courseInstructor import CourseInstructor
from app.models.eventParticipant import EventParticipant
from app.models.individualRequirement import IndividualRequirement
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.course import Course
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.backgroundCheck import BackgroundCheck
from app.models.programManager import ProgramManager
from app.models.note import Note
from app.models.profileNote import ProfileNote
from app.models.activityLog import ActivityLog

@pytest.mark.integration
def test_setGraduationStatus():
    with mainDB.atomic() as transaction:
        # Create a user to run the tests with
        testUser = User.create(username = 'usrtst',
                           firstName = 'Test',
                           lastName = 'User',
                           bnumber = '03522492',
                           email = 'usert@berea.deu',
                           hasGraduated = False)
        
        # make sure users have the default values of false and not interested, respectively
        assert testUser.hasGraduated == False
        setGraduatedStatus(testUser.username, 1)
        
        testUser = User.get_by_id(testUser.username)
        # make sure setGraduatedStatus works correctly
        assert testUser.hasGraduated == True
        
        # verify unchecking box will restore defaults
        setGraduatedStatus(testUser.username, 0)
        
        testUser = User.get_by_id(testUser.username)
        assert testUser.hasGraduated == False
        transaction.rollback()

@pytest.mark.integration
def test_getGraduationManagementUsers():
    with mainDB.atomic() as transaction:
        # in order to delete Users we have to delete all tables that reference it as well.
        EventRsvp.delete().execute()
        BonnerCohort.delete().execute()
        CeltsLabor.delete().execute()
        CourseParticipant.delete().execute()
        CourseInstructor.delete().execute()
        EventParticipant.delete().execute()
        IndividualRequirement.delete().execute()
        ProgramBan.delete().execute()
        Interest.delete().execute()
        QuestionNote.delete().execute()
        CourseQuestion.delete().execute()
        Course.delete().execute()
        BackgroundCheck.delete().execute()
        ProgramManager.delete().execute()
        ProfileNote.delete().execute()
        Note.delete().execute()
        ActivityLog.delete().execute()
        User.delete().execute()

        testUser1 = User.create(username = 'usrtst1',
                    firstName = 'Test',
                    lastName = 'User',
                    bnumber = '03522492',
                    email = 'usert@berea.deu',
                    rawClassLevel = "Senior",
                    hasGraduated = False) 
        
        testUser2 = User.create(username = 'usrtst2',
                    firstName = 'Test',
                    lastName = 'User',
                    bnumber = '035224921',
                    email = 'usert@berea.deu',
                    rawClassLevel = "Senior",
                    hasGraduated = False) 
        
        testUser3 = User.create(username = 'usrtst3',
                    firstName = 'Test',
                    lastName = 'User',
                    bnumber = '0352249210',
                    email = 'usert@berea.deu',
                    rawClassLevel = "Senior",
                    hasGraduated = True) 
        
        testUser4 = User.create(username = 'usrtst4',
                    firstName = 'Test',
                    lastName = 'User',
                    bnumber = '03522492101',
                    email = 'usert@berea.deu',
                    rawClassLevel = "Freshman",
                    hasGraduated = True) 

        BonnerCohort.create(year=2025, user=testUser1)
        BonnerCohort.create(year=2024, user=testUser2)

        sustainedEngagement = {"username": testUser3,
                                "program": 2,
                                "course": None,
                                "description": None,
                                "term": 3,
                                "requirement": 14,
                                "addedBy": testUser4,
                                "addedOn": "",
                                }
        
        IndividualRequirement.create(**sustainedEngagement)

        actualResult = getGraduationManagementUsers(True)

        # testUser4 is not a senior so they should not be shown.
        assert len(actualResult) == 3

        expectedResult = [
            {
                'user': testUser1,
                'cohort': 2025,
                'minorProgress': False
            },
            {  
                'user': testUser2,
                'cohort': 2024,
                'minorProgress': False
            }, 
            {
                'user': testUser3,
                'cohort': None,
                'minorProgress': True
            }
        ]

        assert expectedResult == actualResult
 
        transaction.rollback()

@pytest.mark.integration
def test_updateHideGraduatedStudents():
    with mainDB.atomic() as transaction:
        updateHideGraduatedStudents("ramsayb2", True)
        transaction.rollback()

@pytest.mark.integration
def test_getHideGraduatedStudentsWhereClause():
    with mainDB.atomic() as transaction:
        getHideGraduatedStudentsWhereClause("ramsayb2")
        transaction.rollback()
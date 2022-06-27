import pytest
from flask import g
from app import app
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.logic.volunteers import setProgramManager
from peewee import DoesNotExist


@pytest.mark.integration
def test_modifyCeltsAdmin():
    user = "agliullovak"
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsAdmin == False
    with app.app_context():
        g.current_user = "ramsayb2"
        addCeltsAdmin(userInTest)
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsAdmin == True
        removeCeltsAdmin(userInTest)
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsAdmin == False

        with pytest.raises(DoesNotExist):
            addCeltsAdmin("blahbah")
        with pytest.raises(DoesNotExist):
            addCeltsAdmin("ksgvoidsid;")

def test_modifyCeltsStudentStaff():
    user = "mupotsal"
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsAdmin == False
    with app.app_context():
        g.current_user = "ramsayb2"
        addCeltsStudentStaff(userInTest)
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsStudentStaff == True
    with app.app_context():
        g.current_user = "ramsayb2"
        removeCeltsStudentStaff(userInTest)
    userInTest = User.get(User.username == user)
    assert userInTest.isCeltsStudentStaff == False
    with app.app_context():
        g.current_user = "ramsayb2"
        with pytest.raises(DoesNotExist):
            addCeltsStudentStaff("asdf")
        with pytest.raises(DoesNotExist):
            removeCeltsStudentStaff("1234")

@pytest.mark.integration
def test_updatedProgramManager():    

    #checking if the user is being updated when added to programs
    user_name = "mupotsal"
    program_id = 1
    action = "add"
    setProgramManager(user_name, program_id, action)
    assert StudentManager.get_or_none(StudentManager.program == program_id, StudentManager.user == user_name) is not None


    # Not a student staff, should not be added as a program manager
    user_name2 = "ramsayb2"
    program_id2 = 1
    action2 = "add"
    setProgramManager(user_name2, program_id2, action2)
    assert StudentManager.get_or_none(StudentManager.program==program_id2, StudentManager.user == user_name2) is None

    # if action remove, user should be removed from the table
    user_name3 = "mupotsal"
    program_id3 = 1
    action3 = "remove"
    setProgramManager(user_name3, program_id3, action3)
    assert StudentManager.get_or_none(StudentManager.program==program_id3, StudentManager.user == user_name3) is None
    

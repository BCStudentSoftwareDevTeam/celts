import pytest
from flask import g
from app import app
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager

from peewee import DoesNotExist
from flask import g
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

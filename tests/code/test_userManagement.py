import pytest
from flask import g
from app import app
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term

from peewee import DoesNotExist
from flask import g
@pytest.mark.integration
def test_modifyCeltsAdmin():
    with app.app_context():
        g.current_user = "ramsayb2"
        user = "agliullovak"
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsAdmin == False
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
    with app.app_context():
        g.current_user = "ramsayb2"
        user = "mupotsal"
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsAdmin == False
        addCeltsStudentStaff(userInTest)
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsStudentStaff == True
        removeCeltsStudentStaff(userInTest)
        userInTest = User.get(User.username == user)
        assert userInTest.isCeltsStudentStaff == False

        with pytest.raises(DoesNotExist):
            addCeltsStudentStaff("asdf")
        with pytest.raises(DoesNotExist):
            removeCeltsStudentStaff("1234")

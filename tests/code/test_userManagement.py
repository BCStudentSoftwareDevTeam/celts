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
        current_user = User.get(User.username == user)
        assert current_user.isCeltsAdmin == False
        addCeltsAdmin(current_user)
        current_user = User.get(User.username == user)
        assert current_user.isCeltsAdmin == True
        removeCeltsAdmin(current_user)
        current_user = User.get(User.username == user)
        assert current_user.isCeltsAdmin == False

        with pytest.raises(DoesNotExist):
            addCeltsAdmin("blahbah")
        with pytest.raises(DoesNotExist):
            addCeltsAdmin("ksgvoidsid;")

def test_modifyCeltsStudentStaff():
    with app.app_context():
        g.current_user = "ramsayb2"
        user = "mupotsal"
        current_user = User.get(User.username == user)
        assert current_user.isCeltsAdmin == False
        addCeltsStudentStaff(current_user)
        current_user = User.get(User.username == user)
        assert current_user.isCeltsStudentStaff == True
        removeCeltsStudentStaff(current_user)
        current_user = User.get(User.username == user)
        assert current_user.isCeltsStudentStaff == False

        with pytest.raises(DoesNotExist):
            addCeltsStudentStaff("asdf")
        with pytest.raises(DoesNotExist):
            removeCeltsStudentStaff("1234")

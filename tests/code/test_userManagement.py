import pytest
from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term

from peewee import DoesNotExist
from flask import g
@pytest.mark.integration
def test_modifyCeltsAdmin():
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
    user = "mupotsal"
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == False
    addCeltsStudentStaff(current_user)
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == True
    removeCeltsStudentStaff(current_user)
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == False

    with pytest.raises(DoesNotExist):
        addCeltsStudentStaff("asdf")
    with pytest.raises(DoesNotExist):
        removeCeltsStudentStaff("1234")

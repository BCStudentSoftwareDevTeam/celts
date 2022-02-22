import pytest

from app.logic.userManagement import *
from app.models.user import User
from app.models.term import Term
from app.models.studentManager import StudentManager

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

@pytest.mark.integration
def test_modifyStudentManager():
    user = "mupotsal"
    current_user = User.get(User.username==user)
    currentManagerStatus = StudentManager.get(user=user,program=2)
    assert currentManagerStatus.program.id ==2
    removeProgramManager(user,2)
    assert hasPrivilege(user, 2) == False
    currentManagerStatus = StudentManager.select().where(StudentManager.user==user,StudentManager.program ==2)
    assert currentManagerStatus.exists() == False
    addProgramManager(user,2)
    assert hasPrivilege(user, 2) == True
    currentManagerStatus = StudentManager.get(user=user,program=2)
    assert currentManagerStatus.program.id ==2

def test_changeCurrentTerm():
    # test via g.current_term
    oldTerm = g.current_term
    changeCurrentTerm(2)
    assert g.current_term == 2
    assert not oldTerm

    # test via isCurrentTerm
    oldTerm2 = g.current_term
    newTerm = changeCurrentTerm(1)
    assert newTerm.isCurrentTerm
    assert not oldTerm2 == g.current_term
    assert not oldTerm2.isCurrentTerm

    # reset data back to before test
    changeCurrentTerm(oldTerm)

def test_invalidTermInputs():
    with pytest.raises(DoesNotExist):
        changeCurrentTerm(100)
    with pytest.raises(DoesNotExist):
        changeCurrentTerm("womp")

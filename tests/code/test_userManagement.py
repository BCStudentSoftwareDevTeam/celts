import pytest
from app.logic.userManagement import addCeltsAdmin, removeCeltsAdmin,addCeltsStudentStaff, removeCeltsStudentStaff, changeCurrentTerm, addNextTerm
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

@pytest.mark.integration
def test_addNextTerm():
    newTerm = Term.create(description="Fall 2022",year=2022, academicYear= "2022-2023",isBreak=False, isSummer=False,isCurrentTerm=False)
    newTerm.save()

    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = terms[-1]
    addNextTerm()
    terms = list(Term.select().order_by(Term.id))
    newlyAddedTerm = terms[-1]
    assert newlyAddedTerm.description == "Spring 2023"
    
    query = Term.get(Term.id == lastCreatedTerm)
    query.delete_instance()
    query = Term.get(Term.id == newlyAddedTerm)
    query.delete_instance()

    newTerm = Term.create(description="Fall 2029",year=2029, academicYear= "2029-2030",isBreak=False, isSummer=False,isCurrentTerm=False)
    newTerm.save()

    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = terms[-1]
    addNextTerm()
    terms = list(Term.select().order_by(Term.id))
    newlyAddedTerm = terms[-1]
    assert newlyAddedTerm.description == "Spring 2030"

    query = Term.get(Term.id == lastCreatedTerm)
    query.delete_instance()
    query = Term.get(Term.id == newlyAddedTerm)
    query.delete_instance()

    newTerm = Term.create(description="Spring 2022",year=2022, academicYear= "2021-2022",isBreak=False, isSummer=False,isCurrentTerm=False)
    newTerm.save()

    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = terms[-1]
    addNextTerm()
    terms = list(Term.select().order_by(Term.id))
    newlyAddedTerm = terms[-1]
    assert newlyAddedTerm.description == "Summer 2022"

    query = Term.get(Term.id == lastCreatedTerm)
    query.delete_instance()
    query = Term.get(Term.id == newlyAddedTerm)
    query.delete_instance()

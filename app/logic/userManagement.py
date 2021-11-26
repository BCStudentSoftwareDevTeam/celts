from app.models.user import User
from app.models.term import Term
from app.models.studentManagerPermissions import StudentManagerPermissions
from flask import g, session

from playhouse.shortcuts import model_to_dict

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = True
    user.save()

def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = True
    user.save()

def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()

def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = False
    user.save()

def changeCurrentTerm(term):
    oldCurrentTerm = Term.get_by_id(g.current_term)
    oldCurrentTerm.isCurrentTerm = False
    oldCurrentTerm.save()
    newCurrentTerm = Term.get_by_id(term)
    newCurrentTerm.isCurrentTerm = True
    newCurrentTerm.save()

    session["current_term"] = model_to_dict(newCurrentTerm)

def addProgramManager(user,program):
    user = User.get_by_id(user)
    managerEntry = StudentManagerPermissions.create(user=user,program=program)
    managerEntry.save()

def removeProgramManager(user,program):
    user = User.get_by_id(user)
    delQuery = StudentManagerPermissions.delete().where(StudentManagerPermissions.user == user,StudentManagerPermissions.program == program)
    delQuery.execute()

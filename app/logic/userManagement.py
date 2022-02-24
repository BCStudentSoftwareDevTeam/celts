from app.models.user import User
from app.models.term import Term
from app.models.studentManager import StudentManager
from app.models.program import Program
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
    managerEntry = StudentManager.create(user=user,program=program)
    managerEntry.save()

def removeProgramManager(user,program):
    user = User.get_by_id(user)
    delQuery = StudentManager.delete().where(StudentManager.user == user,StudentManager.program == program)
    delQuery.execute()

def hasPrivilege(user, program):
    user = User.get_by_id(user)
    if StudentManager.select().where(StudentManager.user == user, StudentManager.program == program).exists():
        return True
    else:
        return False

def getPrograms():
    return Program.select().join(StudentManager).where(StudentManager.user==g.current_user).order_by(Program.programName)
def addNextTerm():
    newSemesterMap = {"Spring":"Summer",
                    "Summer":"Fall",
                    "Fall":"Spring"}
    terms = list(Term.select().order_by(Term.id))
    prevTerm = terms[-1]
    prevSemester, prevYear = prevTerm.description.split()

    newYear = int(prevYear) + 1 if prevSemester == "Fall" else int(prevYear)
    newDescription = newSemesterMap[prevSemester] + " " + str(newYear)
    newAY = prevTerm.academicYear

    if prevSemester == "Summer": # we only change academic year when the latest term in the table is Summer
        year1, year2 = prevTerm.academicYear.split("-")
        newAY = year2 + "-" + str(int(year2)+1)

    newTerm = Term.create(
            description=newDescription,
            year=newYear,
            academicYear=newAY,
            isSummer="Summer" in newDescription.split())
    newTerm.save()

    return newTerm

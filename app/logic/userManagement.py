from app.models.user import User
from app.models.term import Term
from flask import g, session
from app.logic.adminLogs import createLog

from playhouse.shortcuts import model_to_dict

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = True
    user.save()
    createLog(f'Made {user.firstName} {user.lastName} a Celts Admin.')


def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = True
    user.save()
    # createLog(f'Made {user.firstName} {user.lastName} a Celts Student Staff.')


def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()
    # createLog(f'Removed {user.firstName} {user.lastName} from Celts Admins.')


def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = False
    user.save()
    # createLog(f'Removed {user.firstName} {user.lastName} from a Celts Student Staff.')


def changeCurrentTerm(term):
    oldCurrentTerm = Term.get_by_id(g.current_term)
    oldCurrentTerm.isCurrentTerm = False
    oldCurrentTerm.save()
    newCurrentTerm = Term.get_by_id(term)
    newCurrentTerm.isCurrentTerm = True
    newCurrentTerm.save()
    session["current_term"] = model_to_dict(newCurrentTerm)
    # createLog(f"Changed Current Term from {oldCurrentTerm.description} to {newCurrentTerm.description}")

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

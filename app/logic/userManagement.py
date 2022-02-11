from app.models.user import User
from app.models.term import Term
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

def addNextTerm():
    terms_table = {"Spring":"Summer",
                    "Summer":"Fall",
                    "Fall":"Spring"}
    terms = list(Term.select().order_by(Term.id))
    lastCreatedTerm = terms[-1]
    termDescription = lastCreatedTerm.description
    lastCreatedTermData = termDescription.split()
    year = lastCreatedTermData[-1]

    if lastCreatedTermData[0]=="Fall": # We only change the year when it is Fall
        year = int(year) + 1

    createdTermDescription = terms_table[lastCreatedTermData[0]]+" "+str(year)
    academicYear = lastCreatedTerm.academicYear
    if lastCreatedTermData[0] == "Summer": #we only change academic year when the latest term in the table is Summer
        previousAY = academicYear.split("-")
        academicYear = str(int(previousAY[0])+1)+"-"+str(int(previousAY[-1])+1)

    isSummer = "Summer" in createdTermDescription.split() 

    newTerm = Term.create(description=createdTermDescription,year=year,academicYear=academicYear, isSummer=isSummer)
    newTerm.save()
    return newTerm

from flask import session, g
from playhouse.shortcuts import model_to_dict
from app.logic.createLogs import createAdminLog
from app.models.term import Term

def addNextTerm():
    newSemesterMap = {"Spring":"Summer",
                      "Summer":"Fall",
                      "Fall":"Spring"}
    terms = list(Term.select().order_by(Term.termOrder))
    prevTerm = terms[-1]
    prevSemester, prevYear = prevTerm.description.split()

    newYear = int(prevYear) + 1 if prevSemester == "Fall" else int(prevYear)
    
    newDescription = newSemesterMap[prevSemester] + " " + str(newYear)
    newAY = prevTerm.academicYear   
    if prevSemester == "Summer ": # we only change academic year when the latest term in the table is Summer
        year1, year2 = prevTerm.academicYear.split("-")
        newAY = year2 + "-" + str(int(year2)+1)

    semester = newDescription.split()[0]
    summer= "Summer" in semester
    newTerm = Term.create(description=newDescription,
                          year=newYear,
                          academicYear=newAY,
                          isSummer= summer,
                          termOrder=Term.convertDescriptionToTermOrder(newDescription))
    newTerm.save()

    return newTerm

def addPastTerm(description):
    semester, year = description.split()
    if 'May' in semester:
        semester = "Summer"
    if semester == "Fall":
        academicYear = year + "-" + str(int(year) + 1)
    elif semester == "Summer" or "Spring":
        academicYear=  str(int(year) - 1) + "-" + year

    isSummer = "Summer" in semester
    newDescription=f"{semester} {year}"
    orderTerm = Term.convertDescriptionToTermOrder(newDescription)
    
    createdOldTerm = Term.create(description= newDescription,
                                 year=year,
                                 academicYear=academicYear,
                                 isSummer=isSummer,
                                 termOrder=orderTerm)
    createdOldTerm.save() 
    return createdOldTerm

def changeCurrentTerm(term):
    oldCurrentTerm = Term.get_by_id(g.current_term)
    oldCurrentTerm.isCurrentTerm = False
    oldCurrentTerm.save()
    newCurrentTerm = Term.get_by_id(term)
    newCurrentTerm.isCurrentTerm = True
    newCurrentTerm.save()
    session["current_term"] = model_to_dict(newCurrentTerm)
    createAdminLog(f"Changed Current Term from {oldCurrentTerm.description} to {newCurrentTerm.description}")
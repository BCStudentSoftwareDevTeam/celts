from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.eventTemplate import EventTemplate
from flask import g, session
from app.logic.adminLogs import createLog
from playhouse.shortcuts import model_to_dict

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = True
    user.save()
    createLog(f'Made {user.firstName} {user.lastName} a CELTS admin member.')


def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = True
    user.save()
    createLog(f'Made {user.firstName} {user.lastName} a CELTS student staff member.')


def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()
    createLog(f'Removed {user.firstName} {user.lastName} from CELTS admins.')


def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = False
    user.save()
    createLog(f'Removed {user.firstName} {user.lastName} from a CELTS student staff member.')


def changeCurrentTerm(term):
    oldCurrentTerm = Term.get_by_id(g.current_term)
    oldCurrentTerm.isCurrentTerm = False
    oldCurrentTerm.save()
    newCurrentTerm = Term.get_by_id(term)
    newCurrentTerm.isCurrentTerm = True
    newCurrentTerm.save()
    session["current_term"] = model_to_dict(newCurrentTerm)
    createLog(f"Changed Current Term from {oldCurrentTerm.description} to {newCurrentTerm.description}")

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
            isSummer="Summer" in newDescription.split(),
            )
    newTerm.save()

    return newTerm

def addOldTerm(description):
    semester, year = description.split()
    if 'May' in semester:
        semester = "Summer"
    if semester == "Fall":
        academicYear = year + "-" + str(int(year) + 1)
    elif semester == "Summer" or "Spring":
        academicYear=  str(int(year) - 1) + "-" + year

    isSummer = "Summer" in semester

    

    orderTerm = year + Term.convertTerm(semester)
    
                
    createdOldTerm = Term.create(
            description=f"{semester} {year}",
            year=year,
            academicYear=academicYear,
            isSummer=isSummer,
            termOrder=orderTerm)
    
    createdOldTerm.save()

    return createdOldTerm

def changeProgramInfo(newProgramName, newContactEmail, newContactName, newLocation, programId):
    """Updates the program info with a new sender and email."""
    program = Program.get_by_id(programId)
    updatedProgram = Program.update({Program.programName:newProgramName, Program.contactEmail: newContactEmail, Program.contactName:newContactName, Program.defaultLocation:newLocation}).where(Program.id==programId)
    updatedProgram.execute()
    if newProgramName != program.programName:
        createLog(f"{program.programName} Program Name was changed to: {newProgramName}")
    if newContactEmail != program.contactEmail:
        createLog(f"{program.programName} Contact Email was changed to: {newContactEmail}")
    if newContactName != program.contactName:
        createLog(f"{program.programName} Contact Name was changed to: {newContactName}")
    if newLocation != program.defaultLocation:
        createLog(f"{program.programName} Location was changed to: {newLocation}")

    return (f'Program email info updated')

def getAllowedPrograms(currentUser):
    """Returns a list of all visible programs depending on who the current user is."""
    if currentUser.isCeltsAdmin:
        return Program.select().order_by(Program.programName)
    else:
        return Program.select().join(ProgramManager).where(ProgramManager.user==currentUser).order_by(Program.programName)



def getAllowedTemplates(currentUser):
    """Returns a list of all visible templates depending on who the current user is. If they are not an admin it should always be none."""
    if currentUser.isCeltsAdmin:
        return EventTemplate.select().where(EventTemplate.isVisible==True).order_by(EventTemplate.name)
    else:
        return []
        

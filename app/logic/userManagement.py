from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.program import Program
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

def addProgramManager(user,program):
    user = User.get_by_id(user)
    managerEntry = ProgramManager.create(user=user,program=program)
    managerEntry.save()
    return(f'{user} added as manager')

def removeProgramManager(user,program):
    user = User.get_by_id(user)
    delQuery = ProgramManager.delete().where(ProgramManager.user == user,ProgramManager.program == program)
    delQuery.execute()
    return (f'{user} removed from managers')

def hasPrivilege(user, program):
    user = User.get_by_id(user)
    if ProgramManager.select().where(ProgramManager.user == user, ProgramManager.program == program).exists():
        return True
    else:
        return False

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

def changeProgramInfo(newEmail, newSender, programId):
    """Updates the program info with a new sender and email."""
    updatedProgram = Program.update({Program.emailReplyTo: newEmail, Program.emailSenderName:newSender}).where(Program.id==programId)
    updatedProgram.execute()
    return (f'Program email info updated')

def getPrograms(currentUser):
    return Program.select().join(ProgramManager).where(ProgramManager.user==currentUser).order_by(Program.programName)

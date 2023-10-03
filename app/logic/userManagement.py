from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.eventTemplate import EventTemplate
from flask import g, session
from app.logic.createLogs import createAdminLog
from playhouse.shortcuts import model_to_dict

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = True
    user.save()
    createAdminLog(f'Made {user.firstName} {user.lastName} a CELTS admin member.')


def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = True
    user.save()
    createAdminLog(f'Made {user.firstName} {user.lastName} a CELTS student staff member.')


def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()
    createAdminLog(f'Removed {user.firstName} {user.lastName} from CELTS admins.')


def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    programManagerRoles = list([obj.program.programName for obj in ProgramManager.select(Program).join(Program).where(ProgramManager.user == user)])
    programManagerRoles = ", ".join(programManagerRoles)
    ProgramManager.delete().where(ProgramManager.user_id == user).execute()
    user.isCeltsStudentStaff = False
    user.save()
    createAdminLog(f'Removed {user.firstName} {user.lastName} from a CELTS student staff member'+ 
                   (f', and as a manager of {programManagerRoles}.' if programManagerRoles else "."))


def changeProgramInfo(newProgramName, newContactEmail, newContactName, newLocation, programId):
    """Updates the program info with a new sender and email."""
    program = Program.get_by_id(programId)
    updatedProgram = Program.update({Program.programName:newProgramName, Program.contactEmail: newContactEmail, Program.contactName:newContactName, Program.defaultLocation:newLocation}).where(Program.id==programId)
    updatedProgram.execute()
    if newProgramName != program.programName:
        createAdminLog(f"{program.programName} Program Name was changed to: {newProgramName}")
    if newContactEmail != program.contactEmail:
        createAdminLog(f"{program.programName} Contact Email was changed to: {newContactEmail}")
    if newContactName != program.contactName:
        createAdminLog(f"{program.programName} Contact Name was changed to: {newContactName}")
    if newLocation != program.defaultLocation:
        createAdminLog(f"{program.programName} Location was changed to: {newLocation}")

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
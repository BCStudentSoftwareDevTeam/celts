from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.eventTemplate import EventTemplate
from flask import g, session, flash
from app.logic.createLogs import createAdminLog
from playhouse.shortcuts import model_to_dict
from typing import List

def addCeltsAdmin(user: str) -> None:
    if user.isCeltsAdmin:
        raise Exception(f"{user.fullName} is already a CELTS Admin.")
    elif user.isStudent and not user.isCeltsStudentStaff: 
        raise Exception(f"{user.fullName} cannot be added as CELTS Admin.")
    else: 
        user: User = User.get_by_id(user)
        user.isCeltsAdmin = True
        user.save()
        createAdminLog(f'Made f"{user.fullName} a CELTS admin member.')        

def addCeltsStudentStaff(user: str) -> None:
    if user.isCeltsStudentStaff:
        raise Exception(f"{user.fullName} is already a CELTS Student Staff.")
    elif user.isStudent:
        user: User = User.get_by_id(user)
        user.isCeltsStudentStaff = True
        user.save()
        createAdminLog(f'Made f"{user.fullName} a CELTS Student Staff.')
    else: 
        raise Exception(f"{user.fullName} cannot be added as CELTS Student Staff.")
    

def addCeltsStudentAdmin(user: str) -> None:
    if user.isCeltsStudentAdmin:
        raise Exception(f"{user.fullName} is already a CELTS Student Admin.")
    elif user.isStudent: 
        user: User = User.get_by_id(user)
        user.isCeltsStudentAdmin = True
        user.save()
        createAdminLog(f'Made {user.fullName} a CELTS Student Admin.')
    else: 
        raise Exception(f"{user.fullName} cannot be added as CELTS Student Admin.")
        

def removeCeltsAdmin(user: str) -> None:
    user: User = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()
    createAdminLog(f'Removed f"{user.fullName} from CELTS admins.')
    
def removeCeltsStudentStaff(user: str) -> None:
    user: User = User.get_by_id(user)
    programManagerRoles: List[str] = list([obj.program.programName for obj in ProgramManager.select(Program).join(Program).where(ProgramManager.user == user)])
    programManagerRoles: str = ", ".join(programManagerRoles)
    ProgramManager.delete().where(ProgramManager.user_id == user).execute()
    user.isCeltsStudentStaff = False
    user.save()
    createAdminLog(f'Removed {user.firstName} {user.lastName} from a CELTS student staff member'+ 
                   (f', and as a manager of {programManagerRoles}.' if programManagerRoles else "."))

def removeCeltsStudentAdmin(user: str) -> None:
    user: User = User.get_by_id(user)
    user.isCeltsStudentAdmin = False
    user.save()
    createAdminLog(f'Removed f"{user.fullName} from a CELTS student admins.')

def changeProgramInfo(newProgramName: str, newContactEmail: str, newContactName: str, newLocation: str, programId: int) -> str:
    """Updates the program info with a new sender and email."""
    program: Program = Program.get_by_id(programId)
    Program.update({Program.programName:newProgramName, Program.contactEmail: newContactEmail, Program.contactName:newContactName, Program.defaultLocation:newLocation}).where(Program.id == programId).execute()
    if newProgramName != program.programName:
        createAdminLog(f"{program.programName} Program Name was changed to: {newProgramName}")
    if newContactEmail != program.contactEmail:
        createAdminLog(f"{program.programName} Contact Email was changed to: {newContactEmail}")
    if newContactName != program.contactName:
        createAdminLog(f"{program.programName} Contact Name was changed to: {newContactName}")
    if newLocation != program.defaultLocation:
        createAdminLog(f"{program.programName} Location was changed to: {newLocation}")

    return (f'Program email info updated')

def getAllowedPrograms(currentUser: User) -> List[Program]:
    """Returns a list of all visible programs depending on who the current user is."""
    if currentUser.isCeltsAdmin:
        return list(Program.select().order_by(Program.programName))
    elif currentUser.isCeltsStudentAdmin:
        return list(Program.select().where(Program.programName != "Bonner Scholars").order_by(Program.programName))
    else:
        return list(Program.select().join(ProgramManager).where(ProgramManager.user==currentUser).order_by(Program.programName))


def getAllowedTemplates(currentUser: User) -> List[EventTemplate]:
    """Returns a list of all visible templates depending on who the current user is. If they are not an admin it should always be none."""
    if currentUser.isCeltsAdmin or currentUser.isCeltsStudentAdmin:
        return EventTemplate.select().where(EventTemplate.isVisible==True).order_by(EventTemplate.name)
    else:
        return []
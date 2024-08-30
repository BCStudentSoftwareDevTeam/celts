from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.eventTemplate import EventTemplate
from flask import g, session
from app.logic.createLogs import createActivityLog
from playhouse.shortcuts import model_to_dict
from app.logic.fileHandler import FileHandler

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = True
    user.save()
    createActivityLog(f'Made {user.firstName} {user.lastName} a CELTS admin member.')


def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = True
    user.save()
    createActivityLog(f'Made {user.firstName} {user.lastName} a CELTS student staff member.')


def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()
    createActivityLog(f'Removed {user.firstName} {user.lastName} from CELTS admins.')


def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    programManagerRoles = list([obj.program.programName for obj in ProgramManager.select(Program).join(Program).where(ProgramManager.user == user)])
    programManagerRoles = ", ".join(programManagerRoles)
    ProgramManager.delete().where(ProgramManager.user_id == user).execute()
    user.isCeltsStudentStaff = False
    user.save()
    createActivityLog(f'Removed {user.firstName} {user.lastName} from a CELTS student staff member'+ 
                   (f', and as a manager of {programManagerRoles}.' if programManagerRoles else "."))

def changeProgramInfo(programId, 
                      attachment, 
                      programName= None, 
                      programDescription = None, 
                      partner = None, 
                      contactEmail=None, 
                      contactName= None, 
                      location = None,
                      instagramUrl = None, 
                      facebookUrl = None, 
                      bereaUrl = None): 
  

    """Updates the program info and logs that change"""
    program = Program.get_by_id(programId) 
    if attachment:
        addFile: FileHandler = FileHandler(attachment, programId=programId)
        addFile.saveFiles()
    updatedProgram = Program.update(
      { Program.programName:programName,
        Program.programDescription: programDescription, 
        Program.partner: partner, 
        Program.contactEmail: contactEmail, 
        Program.contactName: contactName,
        Program.defaultLocation: location,
        Program.coverImage: attachment,
        Program.instagramUrl:instagramUrl,
        Program.facebookUrl: facebookUrl,
        Program.bereaUrl: bereaUrl
      }
        ).where(Program.id==programId)    
    updatedProgram.execute()
  
   
    if programName != program.programName:
        createActivityLog(f"{program.programName} Program Name was changed to: {programName}")
    if programDescription != program.programDescription:
        createActivityLog(f"{program.programName} Description was changed to: {programDescription}")
    if partner != program.partner:
        createActivityLog(f"{program.programName} Program Partner was changed to: {partner}")
    if contactEmail != program.contactEmail:
        createActivityLog(f"{program.programName} Contact Email was changed to: {contactEmail}")
    if contactName != program.contactName:
        createActivityLog(f"{program.programName} Contact Name was changed to: {contactName}")
    if location != program.defaultLocation:
        createActivityLog(f"{program.programName} Location was changed to: {location}")
    

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

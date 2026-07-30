import datetime
from flask import abort, g, session
from playhouse.shortcuts import DoesNotExist, model_to_dict
import xlsxwriter

from app import app
from app.logic.participants import getParticipantsForProgramForAY, getTrainingsForInterestedParticipants
from app.logic.users import getProgramInterest
from app.logic.volunteerSpreadsheet import makeDataXls
from app.models.user import User
from app.models.term import Term
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.eventTemplate import EventTemplate
from app.models.attachmentUpload import AttachmentUpload
from app.logic.createLogs import createActivityLog
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
    
def generateSheetData(program, academicYear, rosterType):
    columns = []
    if rosterType == "Interested Volunteers":
        columns = ["Username",
                   "B-number",
                   "Email",
                   "Phone",
                   "First Name",
                   "Last Name",
                   "CPO",
                   "Major",
                   "Class Level",
                   "Dietary Restrictions",
                   "Handbook Signature",
                   "All Volunteers Training",
                   "Program Specific Training",
                   "Background Check",
                   "Eligible"
                   ]
        query = getTrainingsForInterestedParticipants(program, getProgramInterest(program))
        query = cleanInterestedParticipantsData(query)
        return (columns, query)
    elif rosterType == "Engaged Volunteers" or rosterType == "Last Year Volunteers":
        columns = ["Username",
                   "B-number",
                   "Email",
                   "Phone",
                   "First Name",
                   "Last Name",
                   "CPO",
                   "Major",
                   "Class Level",
                   "Dietary Restrictions",
                   "Handbook Signature"
                   ]
        if rosterType == "Last Year Volunteers":
            academicYear = Term.select().where(Term.academicYear == academicYear).get().previousAcademicYear
        query = getParticipantsForProgramForAY(program, academicYear)
        query = [model_to_dict(user, only=(User.username, User.bnumber, User.email, User.phoneNumber, User.firstName, User.lastName, User.cpoNumber, User.major, User.rawClassLevel, User.dietRestriction, User.lastHandbookSignature)) for user in query]
        query = cleanInterestedParticipantsData(query)
        return (columns, query)

def cleanInterestedParticipantsData(query):
    if type(query) == dict:    
        for username, userData in query.items():
            # Dictionary of user object and participation data            
            query[username]["userObj"].major = "Unknown" if not query[username]["userObj"].major else query[username]["userObj"].major
            query[username]["userObj"].rawClassLevel = "Unknown" if not query[username]["userObj"].rawClassLevel  else query[username]["userObj"].rawClassLevel
            query[username]["userObj"].dietRestriction = "Unknown" if not query[username]["userObj"].dietRestriction else query[username]["userObj"].dietRestriction
            query[username]["userObj"].lastHandbookSignature = "Not Signed" if not query[username]["userObj"].lastHandbookSignature else query[username]["userObj"].lastHandbookSignature
            query[username]["allVolunteer"] = "No" if query[username]["allVolunteer"] == False else "Yes"
            query[username]["programSpecific"] = "No" if query[username]["programSpecific"] == False else "Yes"
            query[username]["eligible"] = "No" if query[username]["eligible"] == False else "Yes"
            del(query[username]["star"])        # Not needed in spreadsheet
    else:
        # User objects only
        for index, userObj in enumerate(query):
            userObj["major"] = "Unknown" if not userObj["major"] else userObj["major"]
            userObj["rawClassLevel"] = "Unknown" if not userObj["rawClassLevel"] else userObj["rawClassLevel"]
            userObj["dietRestriction"] = "Unknown" if not userObj["dietRestriction"] else userObj["dietRestriction"]
            userObj["lastHandbookSignature"] = "Not Signed" if not userObj["lastHandbookSignature"] else userObj["lastHandbookSignature"]
            query[index] = userObj
    return query


def createSpreadsheetForRosters(academicYear, program):
    try:
        program = Program.get_by_id(program)
    except DoesNotExist:
        raise DoesNotExist
    filepath = f"{app.config['files']['base_path']}/{program.programName.replace(" ", "_")}_rosters_{academicYear}.xlsx"
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})
    makeDataXls("Interested Volunteers", generateSheetData(program, academicYear, "Interested Volunteers"), workbook, sheetDesc=f"This worksheet shows all current students who have indicated interest in {program.programName}")
    makeDataXls(f"Engaged Volunteers ({academicYear})", generateSheetData(program, academicYear, "Engaged Volunteers"), workbook, sheetDesc=f"This worksheet shows all students who have participated in a service hours earning event in {program.programName}")
    makeDataXls(f"Last Year Volunteers", generateSheetData(program, academicYear, "Last Year Volunteers"), workbook, sheetDesc=f"This worksheet shows all current students who participated in a service hours earning event in {program.programName} during the previous academic year")
 
    workbook.close()
    return filepath
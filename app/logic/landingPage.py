import os
from flask import g
from app.models.programManager import ProgramManager
from app.models.program import Program
from app.models.user import User


def getManagerProgramDict(user):
    
    managerRows = (ProgramManager.select(ProgramManager, User, Program)
                                 .join(User)
                                 .switch(ProgramManager)
                                 .join(Program))
    programs = Program.select().order_by(Program.programName)
    if not (user.isAdmin or user.isBonnerScholar):
        programs = programs.where(Program.isBonnerScholars == False)
        managerRows = managerRows.where(ProgramManager.program.isBonnerScholars == False)  
    managerProgramDict = {}

    for program in programs:
        managerProgramDict[program] = {"managers": "", "image": os.path.join('static', 'images/logos/celts_symbol.png')}
        with os.scandir("./app/static/images/landingPage") as it:
            for entry in it:
                if entry.name.split('.')[0] == f'{program.programName}':
                    managerProgramDict[program]["image"] = os.path.join('static', f'images/landingPage/{entry.name}')
                    break
    for row in managerRows:
        if managerProgramDict[row.program]["managers"] == "":
            managerProgramDict[row.program]["managers"] = f'{row.user.firstName} {row.user.lastName}'
        else:
            managerProgramDict[row.program]["managers"] = f'{managerProgramDict[row.program]["managers"]}, {row.user.firstName} {row.user.lastName}'
    return managerProgramDict

def getActiveEventTab(programID):
    program = Program.get_by_id(programID)
    if program.isBonnerScholars:
        return "bonnerScholarsEvents"
    elif program.isStudentLed:
        return "studentLedEvents"
    else:
        return "otherEvents"

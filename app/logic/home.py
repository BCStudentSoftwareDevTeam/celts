import os
from flask import g
from app.models.programManager import ProgramManager
from app.models.program import Program

def getManagerProgramDict():
    programs = Program.select()
    managerRows = list(ProgramManager.select())
    managerProgramDict = {}

    for program in programs:
        managerProgramDict[program] = {"managers": "Nobody", "image": os.path.join('static', 'images/celts_symbol.png')}
        with os.scandir("./app/static/images") as it:
            for entry in it:
                if entry.name == f'{program.programName}.jpg':
                    managerProgramDict[program]["image"] = os.path.join('static', f'images/{program.programName}.jpg')
                    break
                elif entry.name == f'{program.programName}.png':
                    managerProgramDict[program]["image"] = os.path.join('static', f'images/{program.programName}.png')
                    break
    for row in managerRows:
        if managerProgramDict[row.program]["managers"] == "Nobody":
            managerProgramDict[row.program]["managers"] = f'{row.user.firstName} {row.user.lastName}'
        else:
            managerProgramDict[row.program]["managers"] = f'{managerProgramDict[row.program]["managers"]}, {row.user.firstName} {row.user.lastName}'
    return managerProgramDict

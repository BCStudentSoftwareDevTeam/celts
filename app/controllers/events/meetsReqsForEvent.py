# boolean function: are you allowed to do the event?
# Check for what event you want to do -Issue 3.8 S&S
# Get all required trainings for that event
# check if (1) you're not banned or (2)
# if so: true
# if you're banned: false
from app.models.user import User
from app.models.programBan import ProgramBan
from app.models.programEvent import ProgramEvent

def isEligibleForProgram(event, user):

    # Find a program that the event belongs to
    program = ProgramEvent.select(ProgramEvent.program).where(ProgramEvent.event == event)  # assuming that the event belongs to one program
    # See if the user is banned from that program
    # If banned, return False
    # Find all the events that are required for the program
    # Did the user attend that event
    # If not, reurn false
    # return true
    if (ProgramBan.select().where(ProgramBan.user == user)) and (ProgramBan.select().where(ProgramBan.program == program)):
        return False
    # req_list = [] # check if class is required, if so add it to the list
    # if ProgramEvent.isRequiredForProgram:
    #     req_list.append()
    # for requirement in req_list:
    #     if not ProgramEvent.isRequiredForProgram:
    #         return False
    return True

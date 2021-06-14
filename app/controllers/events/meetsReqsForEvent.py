# boolean function: are you allowed to do the event?
# Check for what event you want to do -Issue 3.8 S&S
# Get all required trainings for that event
# check if (1) you're not banned or (2)
# if so: true
# if you're banned: false
from app.models.user import User
from app.models.programBan import ProgramBan
from app.models.programEvent import ProgramEvent
def isEligibleForProgram(event):
    if ProgramBan.user == User:
        return False
    req_list = [] # check if class is required, if so add it to the list
    if ProgramEvent.isRequiredForProgram:
        req_list.append()
    for requirement in req_list:
        if not_completed:
            return False
        else:
            return True

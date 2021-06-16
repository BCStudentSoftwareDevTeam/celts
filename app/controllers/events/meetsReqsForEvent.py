# boolean function: are you allowed to do the event?
# Check for what event you want to do -Issue 3.8 S&S
# Get all required trainings for that event
# check if (1) you're not banned or (2)
# if so: true
# if you're banned: false
from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.preqForProgram import PreqForProgram

def isEligibleForProgram(event, user):

    # Find a program that the event belongs to
    program = Event.select(Event.program).where(Event.id == event)  # assuming that the event belongs to one program
    # See if the user is banned from that program
    # If banned, return False
    if (ProgramBan.select().where(ProgramBan.user == user)) and (ProgramBan.select().where(ProgramBan.program == program)):
        return False
    # Find all the events that are required for the program
    # Did the user attend that event
    # If not, reurn false
    for requirement in PreqForProgram.select().where(PreqForProgram.event == event):
        if not EventParticipant.select().where(EventParticipant.attended == True):
            return False
    return True

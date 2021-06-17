from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.preqForProgram import PreqForProgram

def isEligibleForProgram(event, user):

    program = Event.select(Event.program).where(Event.id == event)  # assuming that the event belongs to one program

    if (ProgramBan.select().where(ProgramBan.user == user)) and (ProgramBan.select().where(ProgramBan.program == program)):
        return False

    for requirement in PreqForProgram.select().where(PreqForProgram.event == event):
        if not EventParticipant.select().where(EventParticipant.attended == True):
            return False
    return True

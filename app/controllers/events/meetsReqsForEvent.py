from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.preqForProgram import PreqForProgram

def isEligibleForProgram(event, user):
    """
    Checks if the user is banned from an event. Checks if the user has completed
    specific prerequisite for the event.
    :param event: the name of the event that is passed in
    :param user: the user that is logged into the system
    :return: True if the user is not banned and meets the requirements, and False otherwise
    """

    program = Event.select(Event.program).where(Event.id == event)
    # assuming that the event belongs to one program

    if (ProgramBan.select().where(ProgramBan.user == user)) and
    (ProgramBan.select().where(ProgramBan.program == program)):
        return False

    for requirement in PreqForProgram.select().where(PreqForProgram.event == event):
        if not EventParticipant.select().where(EventParticipant.attended == True):
            return False
    return True

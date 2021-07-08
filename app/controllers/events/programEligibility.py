from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.program import Program


def isEligibleForProgram(program, user):
    """
    Checks if the user is banned from an event. Checks if the user has completed
    specific prerequisite(s) for the event.
    :param program: the id of the program that is passed in
    :param user: the user that is logged into the system
    :return: True if the user is not banned and meets the requirements, and False otherwise
    """
    user = User.get_by_id(user)
    programid = Program.get_by_id(program)

    if (ProgramBan.select().where(ProgramBan.user == user)) and (ProgramBan.select().where(ProgramBan.program == programid)):
        return False

    #Check for events that are prerequisite for program
    #If that event is not attended return False
    #cases: no required events, not attended
    for requirement in Event.select().where(Event.isPrerequisiteForProgram == True):
        print(requirement)
        if not EventParticipant.select().where(EventParticipant.attended == True):
            return False
    return True

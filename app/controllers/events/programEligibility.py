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
    program = Program.get_by_id(program)

    if (ProgramBan.select().where(ProgramBan.user == user)) and (ProgramBan.select().where(ProgramBan.program == program)):
        return False

    # Check for events that are prerequisite for program
    requiredEvents = Event.select().where((Event.isPrerequisiteForProgram == True) & (Event.program == program))

    if requiredEvents:
        for event in requiredEvents:
            # If requiredEvent(s) is not attended return False
            if not EventParticipant.select().where((EventParticipant.attended == True) & (EventParticipant.user == user) & (EventParticipant.event == event.id)):
                return False

    return True

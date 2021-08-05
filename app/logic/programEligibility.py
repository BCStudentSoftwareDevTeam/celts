from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.program import Program
from app.models.programEvent import ProgramEvent


def isEligibleForProgram(program, user):
    """
    Verifies if a given user is eligible for a program by checking if they are
    banned from a program.

    :param program: accepts a Program object or a valid programid
    :param user: accepts a User object or userid
    :return: True if the user is not banned and meets the requirements, and False otherwise
    """

    if (ProgramBan.select().where(ProgramBan.user == user, ProgramBan.program == program).exists()):
        return False

    return True

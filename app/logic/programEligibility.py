from app.models.user import User
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.programBan import ProgramBan
from app.models.program import Program
from app.models.programEvent import ProgramEvent


def isEligibleForProgram(program, user):
    """
    Verifies if a given user is eligible for a program by checking if they are
    banned from a program and if they have attended all the required events for a program.

    :param program: accepts a Program object or a valid programid
    :param user: accepts a User object or userid
    :return: True if the user is not banned and meets the requirements, and False otherwise
    """
    user = User.get_by_id(user)
    program = Program.get_by_id(program)

    if (ProgramBan.select().where(ProgramBan.user == user)) and (ProgramBan.select().where(ProgramBan.program == program)):
        return False

    # Check for events that are prerequisite for program
    requiredEvents = (Event.select(Event)
                           .join(ProgramEvent)
                           .where((Event.isTraining == True) & (ProgramEvent.program == program)))

    if requiredEvents:
        for event in requiredEvents:
            attendedRequiredEvents = (EventParticipant.select().where((EventParticipant.attended == True)
                                    & (EventParticipant.user == user) & (EventParticipant.event == event)))
            if not attendedRequiredEvents:
                return requiredEvents
    return True

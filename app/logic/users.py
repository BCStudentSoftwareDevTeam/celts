from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.note import Note
import datetime

def isEligibleForProgram(program, user):
    """
    Verifies if a given user is eligible for a program by checking if they are
    banned from a program.

    :param program: accepts a Program object or a valid programid
    :param user: accepts a User object or userid
    :return: True if the user is not banned and meets the requirements, and False otherwise
    """
    now = datetime.datetime.now()
    if (ProgramBan.select().where(ProgramBan.user == user, ProgramBan.program == program, ProgramBan.endDate > now).exists()):
        return False

    return True

def addRemoveInterest(rule, program_id, username):
    """
    This function is used to add or remove interest from the interest table.
    Parameters:
    rule: Gets the url from the ajax call, specifies to add or remove interest
    program_id: id of the program the user is interested in
    """
    if 'addInterest' in str(rule):
        Interest.get_or_create(program = program_id, user = username)
        return "Successfully added interest"

    elif 'deleteInterest' in str(rule):
        try:
            deleted_interest = Interest.get(Interest.program == program_id, Interest.user == username)
            deleted_interest.delete_instance()
            return "Successfully removed interest"
        except:
            return "This interest does not exist"


def banUnbanUser(banOrUnban, program_id, username, note, banEndDate, creator):
    """
    This function creates an entry in the note table and programBan table in order
    to ban the selected user.
    Parameters:
    banOrUnban: contains "Ban" or "Unban" to determine which action must be taken
    program_id: primary id of the program the user has been banned or unbanned.
    username: username of the user to be banned or unbanned
    note: note left about the ban or unban, expected to be a reason why the action is needed
    banEndDate: date when the ban will end
    creator: who banned or unbanned the user
    """
    noteForDb  = Note.create(createdBy = creator,
                            createdOn = datetime.datetime.now(),
                            noteContent = note,
                            isPrivate = 0)
    if banOrUnban == "Ban":
        ProgramBan.create(program = program_id,
                          user = username,
                          endDate = banEndDate,
                          banNote = noteForDb.id)
        return "Successfully banned the user"

    else:
        ProgramBan.update(endDate = datetime.datetime.now(),
                                    unbanNote = noteForDb.id).where(ProgramBan.program == program_id,
                                                                    ProgramBan.user == username,
                                                                    ProgramBan.endDate >  datetime.datetime.now()).execute()
        return "Successfully unbanned the user"

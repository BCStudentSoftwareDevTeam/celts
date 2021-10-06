from app.models.programBan import ProgramBan
from app.models.interest import Interest

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


def banUnbanUser(rule, program_id, username):
    """
    This function is ued to add the reasons for being ban and the end date of the ban to the programban table.
    Parameters:
    program_id: id of the program the user has been banned or unbanned.
    """
    if 'banUser' in str(rule):
        ProgramBan.get_or_create(program = program_id, user = username)
        return "Successfully banned the user"

    else:
        deleted_unbanUser = ProgramBan.get(program = program_id, user = username)
        deleted_unBanUser.delete_instance()
        return "Successfully unbanned user"

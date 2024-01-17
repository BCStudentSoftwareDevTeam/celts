from app.models.user import User
from app.models.event import Event
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.models.note import Note
from app.models.user import User
from app.models.profileNote import ProfileNote
from app.models.backgroundCheck import BackgroundCheck
from app.models.backgroundCheckType import BackgroundCheckType
from app.logic.volunteers import addUserBackgroundCheck
import datetime
from peewee import JOIN
from dateutil import parser
from flask import g


def isEligibleForProgram(program, user):
    """
    Verifies if a given user is eligible for a program by checking if they are
    banned from a program.

    :param program: accepts a Program object or a valid programid
    :param user: accepts a User object or userid
    :return: True if the user is not banned and meets the requirements, and False otherwise
    """
    now = datetime.datetime.now()
    if (ProgramBan.select().where(ProgramBan.user == user, ProgramBan.program == program, ProgramBan.endDate > now, ProgramBan.unbanNote == None).exists()):
        return False
    return True

def addUserInterest(program_id, username):
    """
    This function is used to add an interest to .
    Parameters:
    program_id: id of the program the user is interested in
    username: username of the user showing interest
    """
    Interest.get_or_create(program = program_id, user = username)
    return True

def removeUserInterest(program_id, username):
    """
    This function is used to add or remove interest from the interest table.
    Parameters:
    program_id: id of the program the user is interested in
    username: username of the user showing disinterest

    """
    interestToDelete = Interest.get_or_none(Interest.program == program_id, Interest.user == username)
    if interestToDelete:
        interestToDelete.delete_instance()
    return True

def getBannedUsers(program):
    """
    This function returns users banned from a program.
    """
    return ProgramBan.select().where(ProgramBan.program == program, ProgramBan.unbanNote == None)

def isBannedFromEvent(username, eventId):
    """
    This function returns whether the user is banned from the program associated with an event.
    """
    program = Event.get_by_id(eventId).program
    user = User.get(User.username == username)
    return not isEligibleForProgram(program, user)

def banUser(program_id, username, note, banEndDate, creator):
    """
    This function creates an entry in the note table and programBan table in order
    to ban the selected user.
    Parameters:
    program_id: primary id of the program the user has been banned from
    username: username of the user to be banned
    note: note left about the ban, expected to be a reason why the change is needed
    banEndDate: date when the ban will end
    creator: the admin or person with authority who created the ban
    """
    noteForDb = Note.create(createdBy = creator,
                            createdOn = datetime.datetime.now(),
                            noteContent = note,
                            isPrivate = 0,
                            noteType = "ban")

    ProgramBan.create(program = program_id,
                      user = username,
                      endDate = banEndDate,
                      banNote = noteForDb)

def unbanUser(program_id, username, note, creator):
    """
    This function creates an entry in the note table and programBan table in order
    to unban the selected user.
    Parameters:
    program_id: primary id of the program the user has been unbanned from
    username: username of the user to be unbanned
    note: note left about the ban, expected to be a reason why the change is needed
    creator: the admin or person with authority who removed the ban
    """
    noteForDb = Note.create(createdBy = creator,
                            createdOn = datetime.datetime.now(),
                            noteContent = note,
                            isPrivate = 0,
                            noteType = "unban")
    (ProgramBan.update(endDate = datetime.datetime.now(),
                       unbanNote = noteForDb)
               .where(ProgramBan.program == program_id,
                      ProgramBan.user == username,
                      ProgramBan.endDate >  datetime.datetime.now())).execute()

def getUserBGCheckHistory(username):
    """
    Get a users background check history
    """
    bgHistory = {'CAN': [], 'FBI': [], 'SHS': [], 'BSL': []}

    allBackgroundChecks = (BackgroundCheck.select(BackgroundCheck, BackgroundCheckType)
                                          .join(BackgroundCheckType)
                                          .where(BackgroundCheck.user == username)
                                          .order_by(BackgroundCheck.dateCompleted.desc()))
    for row in allBackgroundChecks:
        bgHistory[row.type_id].append(row)

    return bgHistory

def addProfileNote(visibility, bonner, noteTextbox, username):
    if bonner:
        visibility = 1 # bonner notes are always admins and the student

    noteForDb = Note.create(createdBy = g.current_user,
                            createdOn = datetime.datetime.now(),
                            noteContent = noteTextbox,
                            noteType = "profile")
    createProfileNote = ProfileNote.create(user = User.get(User.username == username),
                                           note = noteForDb,
                                           isBonnerNote = bonner,
                                           viewTier = visibility)
    return createProfileNote

def deleteProfileNote(noteId):
    return ProfileNote.delete().where(ProfileNote.id == noteId).execute()

def updateDietInfo(username, dietContent):
    """
    Creates or update a user's diet information
    """

    User.update(dietRestriction = dietContent).where(User.username == username).execute()

    return ""

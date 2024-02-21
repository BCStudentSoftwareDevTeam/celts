from peewee import fn

from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.courseInstructor import CourseInstructor
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event
from app.models.programBan import ProgramBan

def getProgramTranscript(username):
    """
    Returns a Program query object containing all the programs for
    the current user.
    """
    # Add up hours earned in a term for each program they've participated in

    EventData = (Event.select(Event, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
                      .join(EventParticipant)
                      .where(EventParticipant.user == username)
                      .group_by(Event.program, Event.term)
                      .order_by(Event.term)
                      .having(fn.SUM(EventParticipant.hoursEarned > 0)))

    # Fetch all ProgramBan objects for the user
    program_bans = ProgramBan.select().where(ProgramBan.user == username)

    # Create a set of program IDs to remove from transcript
    programs_to_remove = {program_ban.program_id for program_ban in program_bans if program_ban.removeFromTranscript}
    print("---------------------------------------", programs_to_remove)
    # Initialize transcriptData dictionary
    transcriptData = {}

    # Iterate through EventData and populate transcriptData
    for event in EventData:
        if event.program.id not in programs_to_remove:  # Check if program should be included
            print(event.program in programs_to_remove, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print('+++++++++++++++++++++++++++++++', event.program)
            print(type(event.program.id), "??????????????????????????????????????????????????")
            if event.program in transcriptData:
                transcriptData[event.program].append([event.term.description, event.hoursEarned])
            else:
                transcriptData[event.program] = [[event.term.description, event.hoursEarned]]

    return transcriptData


# def getProgramTranscript(username):
#     """
#     Returns a Program query object containing all the programs for
#     current user. If removeFromTranscript is True, remove the corresponding program.
#     """
#     # Retrieve transcript data as before
#     EventData = (Event.select(Event, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
#                       .join(EventParticipant)
#                       .where(EventParticipant.user == username)
#                       .group_by(Event.program, Event.term)
#                       .order_by(Event.term)
#                       .having(fn.SUM(EventParticipant.hoursEarned > 0)))

#     transcriptData = {}
#     for event in EventData:
#         # Check if removeFromTranscript is True and if the programID matches the current event's program ID
#         if removeFromTranscript and programID and event.program.id == programID:
#             continue  # Skip this event if it matches the conditions
#         # Only include the program if removeFromTranscript is False or if it's eligible
#         if not removeFromTranscript:
#             if event.program in transcriptData:
#                 transcriptData[event.program].append([event.term.description, event.hoursEarned])
#             else:
#                 transcriptData[event.program] = [[event.term.description, event.hoursEarned]]
#     return transcriptData


def getSlCourseTranscript(username):
    """
    Returns a SLCourse query object containing all the training events for
    current user.
    """

    slCourses = (Course.select(Course, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
                       .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
                       .where(CourseParticipant.user == username)
                       .group_by(Course.courseName, Course.term))

    return slCourses

def getTotalHours(username):
    """
    Get the toal hours from events and courses combined.
    """
    eventHours = (EventParticipant.select(fn.SUM(EventParticipant.hoursEarned))
                                 .where(EventParticipant.user == username)).scalar()
    courseHours =  (CourseParticipant.select(fn.SUM(CourseParticipant.hoursEarned))
                                    .where(CourseParticipant.user == username)).scalar()

    allHours = {"totalEventHours": (eventHours or 0),
                "totalCourseHours": (courseHours or 0),
                "totalHours": (eventHours or 0) + (courseHours or 0)}
    return allHours

def getStartYear(username):
    """
    Returns the users start term for participation in the CELTS organization
    """

    startDate = (EventParticipant.select(Term.year)
                                 .join(Event)
                                 .join(Term).where(EventParticipant.user == username)
               + CourseParticipant.select(Term.year)
                                 .join(Course)
                                 .join(Term)
                                 .where(CourseParticipant.user == username)
                ).order_by(Event.term.year).first()

    if startDate:
        return startDate.event.term.year

    return "N/A"

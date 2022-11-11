from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.courseInstructor import CourseInstructor
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event
from peewee import DoesNotExist, fn, JOIN


def getOtherEventsTranscript(username):
    """
    Returns a Other Events query object containing all the non-program
    events for the current user.
    """

    otherEventsData = list(EventParticipant.select(Event, Term, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
                    .join(Event)
                    .join(ProgramEvent, JOIN.LEFT_OUTER)
                    .join(Program, JOIN.LEFT_OUTER).switch(Event)
                    .join(Term)
                    .where(EventParticipant.user==username,
                    ProgramEvent.program == None)
                    .group_by(Event.term)
                  )

    return [[row.event.term.description, row.hoursEarned] for row in otherEventsData]

def getProgramTranscript(username):
    """
    Returns a Program query object containing all the programs for
    current user.
    """
    # Add up hours earned in a term for each program they've participated in
    programData = (ProgramEvent
        .select(Program, Event, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
        .join(Program)
        .switch(ProgramEvent)
        .join(Event)
        .join(EventParticipant)
        .where(EventParticipant.user == username)
        .group_by(Program, Event.term)
        .order_by(Event.term)
        .having(fn.SUM(EventParticipant.hoursEarned > 0)))
    transcriptData = {}
    for program in programData:
        print("\n\n")
        print(program.program.description)
        print("\n\n")
        if program.program in transcriptData:
            transcriptData[program.program].append([program.event.term.description, program.hoursEarned])
        else:
            transcriptData[program.program] = [[program.event.term.description, program.hoursEarned]]
    return transcriptData

def getAllEventTranscript(username):
    """
    Combines the program transcript and other events transcript into one dict
    for easier display.
    """
    programDict = getProgramTranscript(username)
    allEventsDict = programDict
    otherList = getOtherEventsTranscript(username)
    if otherList:
        allEventsDict["CELTS Sponsored Events"] = otherList
    return allEventsDict


def getSlCourseTranscript(username):
    """
    Returns a SLCourse query object containing all the training events for
    current user.
    """

    slCourses = (Course
        .select(Course, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
        .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
        .where(CourseParticipant.user == username)
        .group_by(Course.courseName, Course.term))

    return slCourses

def getTotalHours(username):
    """
    Get the toal hours from events and courses combined.
    """
    eventHours = EventParticipant.select(fn.SUM(EventParticipant.hoursEarned)).where(EventParticipant.user == username).scalar()
    courseHours =  CourseParticipant.select(fn.SUM(CourseParticipant.hoursEarned)).where(CourseParticipant.user == username).scalar()

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
                    .join(Term).where(CourseParticipant.user == username)).order_by(Event.term.year)

    startDate = startDate.first()
    if startDate:
        return startDate.event.term.year
    return "N/A"

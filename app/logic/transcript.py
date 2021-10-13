from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.courseInstructor import CourseInstructor
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event
from peewee import DoesNotExist, fn


#FIXME: Needs to break hours down by program and term, not just program
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
        .where(EventParticipant.user == username, Event.isTraining == False, Program.isBonnerScholars == False))

    return programData

def getBonnerScholarEvents(username):
    """
    Returns a bonnerData query object containing all the Bonner events for
    current user.
    """
    bonnerData = (EventParticipant
        .select(Program, ProgramEvent, EventParticipant.event,  EventParticipant.hoursEarned)
        .join(ProgramEvent, on=(EventParticipant.event == ProgramEvent.event))
        .join(Program)
        .switch(EventParticipant)
        .join(Event)
        .where(EventParticipant.user == username,  Event.isTraining == False, Program.isBonnerScholars == True))

    return bonnerData

def getSlCourseTranscript(username):
    """
    Returns a SLCourse query object containing all the training events for
    current user.
    """

    SLCourses = (CourseParticipant
        .select(CourseParticipant, CourseParticipant.course)
        .join(Course)
        .where(CourseParticipant.user == username))

    SLCourseInstructor = (CourseInstructor
        .select(CourseInstructor, CourseInstructor.course.alias("courseId"), CourseInstructor.user)
        .join(Course)
        .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
        .switch(CourseInstructor)
        .join(User)
        .where(CourseParticipant.user == username))

    instructorDict = {}
    for i in SLCourseInstructor:
        instructorDict.setdefault(i.courseId, []).append(i.user.firstName + " " + i.user.lastName)


    return SLCourses, instructorDict

def getTrainingTranscript(username):
    """
    Returns a Training query object containing all the training event information for
    current user.
    """

    trainingData = (EventParticipant.select(EventParticipant.event, EventParticipant.hoursEarned)
                                    .join(Event)
                                    .where(EventParticipant.user == username, Event.isTraining))

    return trainingData

def getTotalHour(username):
    """
    Get the toal hours from events and courses combined.

    """

    eventHours = EventParticipant.select(fn.SUM(EventParticipant.hoursEarned)).where(EventParticipant.user == username).scalar()
    courseHours =  CourseParticipant.select(fn.SUM(CourseParticipant.hoursEarned)).where(CourseParticipant.user == username).scalar()
    if eventHours and courseHours:
        totalHours = eventHours + courseHours
        return totalHours
    elif eventHours:
        return eventHours
    elif courseHours:
        return courseHours
    return 0

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

def getUserdata(username):
    """
    Returns the user object the page belongs too.
    """

    userdata = User.get(User.username == username)

    return userdata

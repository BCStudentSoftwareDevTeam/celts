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

def getSlCourseTranscript(username):
    """
    Returns a SLCourse query object containing all the training events for
    current user.
    """
    user = User.get_by_id(username)

    SLCourses = (CourseInstructor
        .select(Course, CourseParticipant, CourseInstructor.user, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
        .join(Course)
        .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
        .where(CourseParticipant.user == user))

    return SLCourses

def getTrainingTranscript(username):
    """
    Returns a Training query object containing all the training event information for
    current user.
    """

    trainingData = (EventParticipant.select(EventParticipant.event, EventParticipant.hoursEarned)
                                    .join(Event)
                                    .where(EventParticipant.user == username, Event.isTraining))

    return trainingData

#FIXME: Needs to break hours down by program and term, not just program
def getProgramTranscript(username):
    """
    Returns a Program query object containing all the training events for
    current user.
    """
    user = User.get_by_id(username)

    # Add up hours earned in a term for each program they've participated in
    hoursQuery = (ProgramEvent
        .select(Program, Event, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
        .join(Program)
        .switch(ProgramEvent)
        .join(Event)
        .join(EventParticipant)
        .where(EventParticipant.user == user, Event.isTraining == False, Program.isBonnerScholars == False))

    return hoursQuery

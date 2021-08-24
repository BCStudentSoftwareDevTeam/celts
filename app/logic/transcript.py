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
    Returns a service-learning course list that contains a name of the course, term,
    list of instructors who teach the course, and hours earned for each course that the user took.
    :user: model object
    """
    user = User.get_by_id(username)
    slCourseInformation = (CourseParticipant
        .select(CourseParticipant.course, CourseParticipant.user, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
        .group_by(CourseParticipant.course, CourseParticipant.user)
        .where(CourseParticipant.user == user))

    allCoursesList = []
    for course in slCourseInformation:
        user_full_name = f"{course.user.firstName} {course.user.lastName}"
        course_name = course.course.courseName
        description = course.course.term.description
        hours = course.hoursEarned
        instructorQuery = CourseInstructor.select().where(CourseInstructor.course == course.course)
        instructorList = [f"{i.user.firstName} {i.user.lastName}" for i in instructorQuery]

        #creates a list for all information of a course that a courseParticipant is involved in
        allCoursesList.append([ user_full_name , course_name , description , hours , instructorList ])

    return allCoursesList


#FIXME: Needs to break hours down by program and term, not just program
def getProgramTranscript(username):
    """
    Returns a list of programs that the user participated in. The list includes a program name,
    term, and hours earned for each program that the user attended.
    :user: model object
    """
    user = User.get_by_id(username)

    # Add up hours earned in a term for each program they've participated in
    hoursQuery = (Program
        .select(Program, Event.term, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
        .join(ProgramEvent)
        .join(Event)
        .join(EventParticipant)
        .where(EventParticipant.user == user)
        .group_by(Program, Event.term))

    return [[p.programName, Term.get_by_id(p.term).description, p.hoursEarned] 
            for p in hoursQuery.objects() ] 

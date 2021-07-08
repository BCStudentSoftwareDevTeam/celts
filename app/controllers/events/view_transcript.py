from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.courseInstructor import CourseInstructor
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event
from peewee import DoesNotExist

from peewee import *

def getSlCourseTranscript(user):
    """
    Returns a service-learning course list that contains a name of the course, term,
    list of instructors who teach the course, and hours earned for each course that the user took.
    :user: model object
    """
    username = User.get_by_id(user)
    slCourseInformation = (CourseParticipant
    .select(CourseParticipant.course, CourseParticipant.user, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
    .group_by(CourseParticipant.course, CourseParticipant.user)
    .where(CourseParticipant.user == username))

    allCoursesList = []
    listOfEachSlCourseInfo = []
    
    for course in slCourseInformation:
        user_full_name = course.user.firstName + " "+ course.user.lastName
        course_name = course.course.courseName
        description = course.course.term.description
        hours = course.hoursEarned
        cInstructor = CourseInstructor.select().where(CourseInstructor.course== course.course)
        instructorList = []
        for instructor in cInstructor.objects():
            instructorList.append(instructor.user.firstName+" "+ instructor.user.lastName)
        #creates a list for all information of a course that a courseParticipant is involved in
        listOfEachSlCourseInfo = [ user_full_name , course_name , description , hours , instructorList ]
        allCoursesList.append(listOfEachSlCourseInfo)

    return allCoursesList


def getProgramTranscript(user):
    """
    Returns a list of programs that the user participated in. The list includes a program name,
    term, and hours earned for each program that the user attended.
    :user: model object
    """
    username = User.get_by_id(user)
    # Add up hours earned for each program they've participated in
    programInformation = (EventParticipant
        .select(EventParticipant.event , fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
        .where(EventParticipant.user == username)
        .join(Event)
        .join(Program)
        .group_by(EventParticipant.event.program))

    listOfProgramsTranscript = []
    programTranscript = []

    for program in programInformation:

        programName = program.event.program.programName
        #FIXME: If there are more than one events for the program and the term.description are different:
            #term = "earliest term - final term"
        term = program.event.term.description
        totalHoursEarnedForProgram = program.hoursEarned
        programTranscript = [ programName , term , totalHoursEarnedForProgram ]
        listOfProgramsTranscript.append(programTranscript)

    return listOfProgramsTranscript

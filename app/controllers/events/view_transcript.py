from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.courseInstructor import CourseInstructor
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event
# from flask import g
from peewee import *
# from playhouse.shortcuts import model_to_dict



def getSLCourseTranscript(user):
    """
    Returns a service-learning course list that contains a name of the course, term,
    list of instructors who teach the course, and hours earned for each course that the user took.
    :user: model object
    """
    sLCourseInformation = (CourseParticipant
    .select(CourseParticipant.course, CourseParticipant.user, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
    .group_by(CourseParticipant.course, CourseParticipant.user)
    .where(CourseParticipant.user== user))
    courses = [item for item in sLCourseInformation.objects()]

    allCoursesList = []
    listOfEachSLCourseInfo = []
    for i in range(0,len(courses)):

        user_full_name = [(courses[i].user.firstName + " "+ courses[i].user.lastName)]
        course_name = courses[i].course.courseName
        description = courses[i].course.term.description
        hours = courses[i].hoursEarned
        courseId = courses[i].course
        cInstructor = CourseInstructor.select().where(CourseInstructor.course==courseId)
        instructorList = []
        for instructor in cInstructor.objects():
            instructorList.append(instructor.user.firstName+" "+ instructor.user.lastName)
        #creates a list for all information of a course that a courseParticipant is involved in
        listOfEachSLCourseInfo = [{"fullName": user_full_name}, {"courseName": course_name}, {"termName": description}, {"cHoursAccrued": hours}, {"cInstructorName": instructorList}]
        allCoursesList.append(listOfEachSLCourseInfo)

    return allCoursesList


def getProgramTranscript(user):
    """
    Returns a list of programs that the user participated in. The list includes a program name,
    term, and hours earned for each program that the user attended.
    :user: model object
    """
    # Add up hours earned for each program they've participated in
    programInformation = (EventParticipant
        .select(EventParticipant.event , fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
        .where(EventParticipant.user == user)
        .join(Event)
        .join(Program)
        .group_by(EventParticipant.event.program)
    )

    listOfProgramsTranscript = []
    programTranscript = []

    for i in range(0, len(programInformation)):
        print(i)
        programname = programInformation[i].event.program.programName
        term = programInformation[i].event.term.description
        cHoursAccrued = programInformation[i].hoursEarned
        programTranscript = [programname, term, cHoursAccrued]
        listOfProgramsTranscript.append(programTranscript)
    print("here", programTranscript)
    print("list", listOfProgramsTranscript)

    #Note: It is kind of wierd to get the term for a program because it has more than one events that might be in different term
    #When do we want to generate a transcript for the students. Is it by the end of each term? year?

    #Note: Create list of list for the trancript

def getUser(user):
    """
    Returns the user's first and last name.
    :user: model object
    """
    return user.firstName + " " + user.lastName

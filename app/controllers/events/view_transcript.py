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
    sLCourseInformation = (CourseParticipant.select(CourseParticipant.course, CourseParticipant.user, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))

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

    programInformation = (EventParticipant
        .select(EventParticipant.user, fn.SUM(EventParticipant.hoursEarned)).alias("sum_hours")
        .group_by(EventParticipant.user)
        .order_by(fn.SUM(EventParticipant.hoursEarned).desc()))

    for eUser in programInformation.tuples():
        print(eUser)


    programsInfo = [item for item in programInformation.objects()]
    print(programsInfo)
    programList = []
    pList = []
    programs = []
    pHoursAccrued = EventParticipant.select(EventParticipant.event).where(EventParticipant.user == user)
    programSumDict = {}
    for event in pHoursAccrued:

        programID = event.event.program.id # the program number associated with the event number
        # print(event.event.term.description)
        # hours = float(event.hoursEarned) # the hours of the event you participated in
        # if event.event.program.programName in programSumDict:
        #     programSumDict[event.event.program.programName] += hours
        # else:
        #     programSumDict[event.event.program.programName] = hours

        if [event.event.program.programName, event.event.program.term.description] not in pList:
            pList.append([event.event.program.programName, event.event.program.term.description])
            programs.append(event.event.program)

    for program in programs:
        pName = program.programName
        pTerm = program.term.description
        programList.append([pName, pTerm])

    return programList

def getUser(user):
    """
    Returns the user's first and last name.
    :user: model object
    """
    return user.firstName + " " + user.lastName

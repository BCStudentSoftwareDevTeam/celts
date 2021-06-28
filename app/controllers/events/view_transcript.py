from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.courseInstructors import CourseInstructors
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event
from flask import g
from peewee import *
from playhouse.shortcuts import model_to_dict



def getSLCourseTranscript(user):
    """
    Returns a service-learning course list that contains a name of the course, term,
    list of instructors who teach the course, and hours earned for each course that the user took.
    :user: model object
    """
    # user = g.current_user

    # hoursEarnedForCourse = (CourseParticipant
    #     .select(CourseParticipant.hoursEarned)
    #     .where(CourseParticipant.user == user))
    #     # .join(Course, on=(CourseParticipant.course.courseName == Course.courseName))
    #     # .switch(CourseParticipant)
    #     # .join(CourseParticipant.user, on=(User == CourseParticipant.user))
    #     # .group_by(CourseParticipant.user)
    #     # .order_by(fn.SUM(CourseParticipant.hoursEarned).desc()))
    # print(hoursEarnedForCourse)

    #Goal: Course Name(Course Table) , Semester(Term Table) , Instructor(CourseInstructors Table), Hours(CourseParticipant)
    sLCourseInformation = (CourseParticipant.select(CourseParticipant.course, CourseParticipant.user, fn.SUM(CourseParticipant.hoursEarned).alias("hoursEarned"))
    # .join(Course)
    # .join(User)
    .group_by(CourseParticipant.course, CourseParticipant.user)
    .where(CourseParticipant.user== user))
    courses = [item for item in sLCourseInformation.objects()]
    return courses
    # sLCourseInformation = (Course.select(Course.courseName)
    #                         .join(CourseParticipant,
    #                                 on=(CourseParticipant.course.courseName == Course.courseName))
    #                         .join(User,
    #                                 on=(User.username==CourseParticipant.username))
    #                         )
    print(courses)
    print(sLCourseInformation)

    # courseList = []
    # cList = []
    # courses = []
    # cHoursAccrued = CourseParticipant.select().where(CourseParticipant.user == user)
    # courseSumDict = {}
    # for course in cHoursAccrued:
    #     hours = float(course.hoursEarned) # the hours of the event you participated in
    #     if course.course.courseName in courseSumDict:
    #         courseSumDict[course.course.courseName] += hours
    #     else:
    #         courseSumDict[course.course.courseName] = hours
    #
    #     if [course.course.courseName, course.course.term.description] not in cList:
    #         cList.append([course.course.courseName, course.course.term.description])
    #         courses.append(course.course)
    #
    # for course in courses:
    #     cName = course.courseName
    #     cTerm = course.term.description
    #     cInstructor = CourseInstructors.select().where(CourseInstructors.course==course)
    #     instructorList = []
    #     for instructor in cInstructor:
    #         instructorList.append(instructor.user.firstName+" "+ instructor.user.lastName)
    #
    #     cHours = courseSumDict[cName]
    #     courseList.append([cName, cTerm, instructorList, cHours])
    #
    # return sLCourseInformation

    # make test, expect dictionary
    # turn the query result into a dictionary to reference by key
    # use list of instructors that we already had outside of query

def getProgramTranscript(user):
    """
    Returns a list of programs that the user participated in. The list includes a program name,
    term, and hours earned for each program that the user attended.
    :user: model object
    """

    query = (EventParticipant
        .select(EventParticipant.user, fn.SUM(EventParticipant.hoursEarned)).alias("sum_hours")
        # .join(Event, on=(EventParticipant.event.eventName == Event.eventName))
        # .switch(EventParticipant)
        # .join(Event)
        # .where(EventParticipant.user == user)
        .group_by(EventParticipant.user)
        .order_by(fn.SUM(EventParticipant.hoursEarned).desc()))
    # print(query)
    for eUser in query.tuples():
        # print(eUser)
        pass


    programList = []
    pList = []
    programs = []
    pHoursAccrued = EventParticipant.select().where(EventParticipant.user == user)
    programSumDict = {}
    for event in pHoursAccrued:

        programID = event.event.program.id # the program number associated with the event number
        # print(event.event.term.description)
        hours = float(event.hoursEarned) # the hours of the event you participated in
        if event.event.program.programName in programSumDict:
            programSumDict[event.event.program.programName] += hours
        else:
            programSumDict[event.event.program.programName] = hours

        if [event.event.program.programName, event.event.program.term.description] not in pList:
            pList.append([event.event.program.programName, event.event.program.term.description])
            programs.append(event.event.program)

    for program in programs:
        pName = program.programName
        pTerm = program.term.description
        pHours = programSumDict[pName]
        programList.append([pName, pTerm, pHours])

    return programList

def getUser(user):
    """
    Returns the user's first and last name.
    :user: model object
    """
    return user.firstName + " " + user.lastName

from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.courseInstructors import CourseInstructors
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.event import Event


def getSLCourseTranscript(user):
    courseList = []
    cList = []
    courses = []
    cHoursAccrued = CourseParticipant.select().where(CourseParticipant.user == user)
    courseSumDict = {}
    for course in cHoursAccrued:
        hours = float(course.hoursEarned) # the hours of the event you participated in
        if course.course.courseName in courseSumDict:
            courseSumDict[course.course.courseName] += hours
        else:
            courseSumDict[course.course.courseName] = hours

        if [course.course.courseName, course.course.term.description] not in cList:
            cList.append([course.course.courseName, course.course.term.description])
            courses.append(course.course)

    for course in courses:
        cName = course.courseName
        cTerm = course.term.description
        cInstructor = CourseInstructors.select().where(CourseInstructors.course==course)
        instructorList = []
        for instructor in cInstructor:
            instructorList.append(instructor.user.firstName+" "+ instructor.user.lastName)

        cHours = courseSumDict[cName]
        courseList.append([cName, cTerm, instructorList, cHours])

    return courseList

def getProgramTranscript(user):
    programList = []
    pList = []
    programs = []
    pHoursAccrued = EventParticipant.select().where(EventParticipant.user == user)
    programSumDict = {}
    for event in pHoursAccrued:

        programID = event.event.program.id # the program number associated with the event number

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
    return user.firstName + " " + user.lastName

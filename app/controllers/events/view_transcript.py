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
    courses = Course.select()
    cHoursAccrued = CourseParticipant.select()
    i=0
    for course in courses:
        cName = course.courseName

        cTerm = course.term.description

        cInstructor = CourseInstructors.select().where(CourseInstructors.course==course)
        instructorList = []
        for instructor in cInstructor:
            instructorList.append(instructor.user.firstName+" "+ instructor.user.lastName)

        cHoursEarned = []
        for hours in cHoursAccrued:
            cHoursEarned.append(hours.hoursEarned)
        if course.isAllSectionsServiceLearning:
            courseList.append([cName, cTerm, instructorList, cHoursEarned[i]])
        i+=1

    if courseList == []:
        return [["", "", [None], ""],
                ["", "", [None], ""],
                ["", "", [None], ""],
                ["", "", [None], ""]]
    else:
        return courseList

def getProgramTranscript(user):
    programList = []
    pList = []
    programs = Program.select()
    pHoursAccrued = EventParticipant.select()
    i = 0
    programSum = 0
    programSumList = []
    for event in pHoursAccrued:
        hours = event.hoursEarned # the hours of the event you participated in

        programSum = float(hours)+programSum
        programSumList.append(programSum)
        # eventID = event.event.id # the event number associated with the event

        programID = event.event.program.id # the program number associated with the event number
        pList.append([event.event.program.programName, event.event.program.term.description])
        print(pList)
    print(programSumList)

    for program in programs:
        pName = program.programName
        pTerm = program.term.description
        pHours = programSumList[i]
        programList.append([pName, pTerm, pHours])
        i += 1
    if programList == []:
        return [["", "", ""],
                ["", "", ""],
                ["", "", ""]]
    else:
        return programList

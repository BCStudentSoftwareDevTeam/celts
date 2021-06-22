from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.courseStatus import CourseStatus
from app.models.program import Program
from app.models.courseInstructors import CourseInstructors
from app.models.user import User
from app.models.event import Event
from app.models.term import Term

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
        return [["", 0], ["", 0], ["", 0], ["", 0]]
    else:
        # print(courseList)
        return courseList

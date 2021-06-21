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
    for course in courses:
        cName = course.courseName
        cTerm = course.term
        if course.isAllSectionsServiceLearning:
            courseList.append([cName, cTerm])

    if courseList == []:
        return [["", 0], ["", 0], ["", 0], ["", 0]]
    else:
        return courseList

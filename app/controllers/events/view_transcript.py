from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.courseStatus import CourseStatus
from app.models.program import Program
from app.models.courseInstructors import CourseInstructors
from app.models.user import User
from app.models.event import Event
from app.models.term import Term

def ViewCourseTranscript():
    courseList = []
    courses = Course.select()
    for course in courses:
        cName = Course.get(Course.courseName == 2)
        cTerm = Course.term
        cAccruedHours = CourseParticipant.hoursEarned
        courseList.append([cName, cTerm, cAccruedHours])
    return courseList

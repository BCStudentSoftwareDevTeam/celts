from app.models.courseInstructor import CourseInstructor
from app.models.courseStatus import CourseStatus
from app.models.course import Course
from app.models.term import Term


def pendingCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    pending courses.
    '''

    pendingCourses = (CourseInstructor.select(Course.courseName, Term.description, CourseInstructor.user, Course.status)
                    .join(Course)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term)).where(CourseInstructor.course.term.id == termId, Course.status.status != "Approve")


    return pendingCourses
def approveCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    pending courses.
    '''

    approveCourses = (CourseInstructor.select(Course.courseName, Term.description, CourseInstructor.user, Course.status)
                    .join(Course)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term)).where(CourseInstructor.course.term.id == termId, Course.status.status == "Approve")


    return approveCourses

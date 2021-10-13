from app.models.courseInstructor import CourseInstructor
from app.models.courseStatus import CourseStatus
from app.models.course import Course
from app.models.term import Term


def pendingCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    non approved and non completed courses.
    '''

    pendingCourses = (CourseInstructor.select(Course.courseName, Term.description, CourseInstructor.user, Course.status)
                    .join(Course)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term)).where(CourseInstructor.course.term.id == termId, Course.status.status != "Approved", Course.status.status != "Completed")



    return pendingCourses


def approvedCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    approved courses.
    '''

    approvedCourses = (CourseInstructor.select(Course.courseName, Course.id, Term.description, CourseInstructor.user, Course.status)
                    .join(Course)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term)).where(CourseInstructor.course.term.id == termId, Course.status.status == "Approved")

    courseIds = []
    for course in approvedCourses:
        courseIds.append(course.course.id)

    approvedCourseInstructor = getinstructorData(courseIds)
    return approvedCourses

def getinstructorData(courseIds):
    """
    Gets and instructor object for the course id's given.
    """

    instructorDict = {}
    for i in SLCourseInstructor:
        instructorDict.setdefault(i.courseId, []).append(i.user.firstName + " " + i.user.lastName)

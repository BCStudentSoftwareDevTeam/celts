from app.models.courseInstructor import CourseInstructor
from app.models.courseStatus import CourseStatus
from app.models.course import Course
from app.models.term import Term


def courseData(termId):
    '''
    Queries the database to get all the neccessary information for
    pending courses.
    '''

    courseData = (CourseInstructor.select(Course.courseName, Term.description, CourseInstructor.user)
                    .join(Course)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term)).where(CourseInstructor.course.term.id == termId)


    return courseData

from flask import flash
from peewee import fn, JOIN

from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.courseStatus import CourseStatus
from app.logic.adminLogs import createLog
from app.models.course import Course
from app.models.term import Term
from app.models.user import User


def unapprovedCourses(termId):
    '''
    Queries the database to get all the neccessary information for submitted courses.
    '''

    unapprovedCourses = (Course.select(Course, Term, CourseStatus, fn.GROUP_CONCAT(" " ,User.firstName, " ", User.lastName).alias('instructors'))
                  .join(CourseInstructor, JOIN.LEFT_OUTER)
                  .join(User, JOIN.LEFT_OUTER).switch(Course)
                  .join(CourseStatus).switch(Course)
                  .join(Term)
                  .where(Term.id == termId,
                         Course.status.in_([CourseStatus.SUBMITTED,
                                            CourseStatus.INCOMPLETE]))
                  .group_by(Course, Term, CourseStatus)
                  .order_by(Course.status))

    return unapprovedCourses
def approvedCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    approved courses.
    '''

    approvedCourses = (Course.select(Course, Term, CourseStatus, fn.GROUP_CONCAT(" " ,User.firstName, " ", User.lastName).alias('instructors'))
                        .join(CourseInstructor, JOIN.LEFT_OUTER)
                        .join(User, JOIN.LEFT_OUTER).switch(Course)
                        .join(CourseStatus).switch(Course)
                        .join(Term)
                        .where(Term.id == termId, Course.status == CourseStatus.APPROVED)
                        .group_by(Course, Term, CourseStatus))

    return approvedCourses

def createCourse(creator="No user provided"):
    """ Create an empty, incomplete course """
    course = Course.create(status=CourseStatus.INCOMPLETE, createdBy=creator)
    for i in range(1, 7):
        CourseQuestion.create( course=course, questionNumber=i)

    return course

def updateCourse(courseData):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instuctors assigned to the course and update the information in the db.
    """
    course = Course.get_by_id(courseData['courseID'])
    for toggler in ["slSectionsToggle", "permanentDesignation"]:
        courseData.setdefault(toggler, "off")
    Course.update(
        courseName=courseData["courseName"],
        courseAbbreviation=courseData["courseAbbreviation"],
        sectionDesignation=courseData["sectionDesignation"],
        courseCredit=courseData["credit"],
        isRegularlyOccurring=int(courseData["isRegularlyOccurring"]),
        term=courseData['term'],
        status=CourseStatus.SUBMITTED,
        previouslyApprovedDescription = courseData["previouslyApprovedDescription"],
        isAllSectionsServiceLearning=("on" in courseData["slSectionsToggle"]),
        serviceLearningDesignatedSections=courseData["slDesignation"],
        isPermanentlyDesignated=("on" in courseData["permanentDesignation"]),
    ).where(Course.id == course.id).execute()
    for i in range(1, 7):
        (CourseQuestion.update(questionContent=courseData[f"{i}"])
                    .where((CourseQuestion.questionNumber == i) &
                           (CourseQuestion.course==course)).execute())
    instructorList = []
    if 'instructor[]' in courseData:
        instructorList = courseData.getlist('instructor[]')
    CourseInstructor.delete().where(CourseInstructor.course == course).execute()
    for instructor in instructorList:
        CourseInstructor.create(course=course, user=instructor)
    createLog(f"Saved SLC proposal: {courseData['courseName']}")
    return Course.get_by_id(course.id)

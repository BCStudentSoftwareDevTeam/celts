from flask import flash

from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.courseStatus import CourseStatus
from app.models.course import Course
from app.models.term import Term


def submittedCourses(termId):
    '''
    Queries the database to get all the neccessary information for submitted courses.
    '''

    submittedCourses = (Course.select(Course, Term)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term).where(Term.id == termId, Course.status == CourseStatus.SUBMITTED).distinct())

    return submittedCourses

def approvedCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    approved courses.
    '''

    approvedCourses = (Course.select(Course, Term)
                        .join(CourseStatus)
                        .switch(Course)
                        .join(Term).where(Term.id == termId, Course.status == CourseStatus.APPROVED).distinct())

    return approvedCourses

def createCourse(courseData, createdBy):
    """This function will create a course given a form."""
    term = Term.get(Term.id==courseData["term"])
    status = CourseStatus.get_by_id(CourseStatus.SUBMITTED)
    for toggler in ["regularOccurenceToggle", "slSectionsToggle", "permanentDesignation"]:
        courseData.setdefault(toggler, "off")
    course = Course.create(
        courseName=courseData["courseName"],
        courseAbbreviation=courseData["courseAbbreviation"],
        courseCredit=courseData["credit"],
        isRegularlyOccuring=("on" in courseData["regularOccurenceToggle"]),
        term=term,
        status=status,
        createdBy=createdBy,
        isAllSectionsServiceLearning=("on" in courseData["slSectionsToggle"]),
        serviceLearningDesignatedSections=courseData["slDesignation"],
        isPermanentlyDesignated=("on" in courseData["permanentDesignation"]),
    )
    for i in range(1, 7):
        CourseQuestion.create(
            course=course,
            questionContent=courseData[f"{i}"],
            questionNumber=i
        )

    instructorList = []
    if 'instructor[]' in courseData: 
        instructorList = courseData.getlist('instructor[]')

    for instructor in instructorList:
        CourseInstructor.create(course=course, user=instructor)
    return course

def updateCourse(courseData):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instuctors assigned to the course and update the information in the db.
    """
    try:
        course= Course.get_by_id(courseData['courseID'])
        for toggler in ["regularOccurenceToggle", "slSectionsToggle", "permanentDesignation"]:
            courseData.setdefault(toggler, "off")

        Course.update(
            courseName=courseData["courseName"],
            courseAbbreviation=courseData["courseAbbreviation"],
            courseCredit=courseData["credit"],
            isRegularlyOccuring=("on" in courseData["regularOccurenceToggle"]),
            term=courseData['term'],
            status=CourseStatus.SUBMITTED,
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
    except:
        return False;

    return course

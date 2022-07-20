from flask import request, render_template, g, abort, json, redirect, jsonify, flash
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.courseStatus import CourseStatus
from app.models.course import Course
from app.models.term import Term


def submittedCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    non approved and non submitted courses.
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

def createCourse(courseData, instructorsDict):
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
        createdBy=g.current_user,
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
    for instructor in instructorsDict["instructors"]:
        CourseInstructor.create(course=course, user=instructor.username)
    return course

def updateCourse(courseData, instructorsDict):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instuctors assigned to the course and update the information in the db.
    """
    try:
        course= Course.get_by_id(courseData['courseID'])
        for toggler in ["regularOccurenceToggle", "slSectionsToggle", "permanentDesignation"]:
            courseData.setdefault(toggler, "off")

        status = CourseStatus.get_by_id(CourseStatus.SUBMITTED)
        Course.update(
            courseName=courseData["courseName"],
            courseAbbreviation=courseData["courseAbbreviation"],
            courseCredit=courseData["credit"],
            isRegularlyOccuring=("on" in courseData["regularOccurenceToggle"]),
            term=courseData['term'],
            status=status,
            isAllSectionsServiceLearning=("on" in courseData["slSectionsToggle"]),
            serviceLearningDesignatedSections=courseData["slDesignation"],
            isPermanentlyDesignated=("on" in courseData["permanentDesignation"]),
        ).where(Course.id == courseData['courseID']).execute()
        for i in range(1, 7):
            (CourseQuestion.update(questionContent=courseData[f"{i}"])
                        .where((CourseQuestion.questionNumber == i) & (CourseQuestion.course==courseData["courseID"])).execute())
        removeInstructors = CourseInstructor.delete().where(CourseInstructor.course == courseData["courseID"]).execute()
        for instructor in instructorsDict["instructors"]:
            if not CourseInstructor.select().where(CourseInstructor.course==courseData["courseID"], CourseInstructor.user==instructor).exists():
                addInstructors = CourseInstructor.create(course=courseData["courseID"], user=instructor)
    except:
        flash("Course not approved!", "danger")
    return course

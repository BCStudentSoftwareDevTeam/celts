from flask import request, render_template, g, abort, json, redirect, jsonify, flash
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.courseStatus import CourseStatus
from app.models.course import Course
from app.models.term import Term


def pendingCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    non approved and non completed courses.
    '''

    pendingCourses = (Course.select(Course, Term)
                    .join(CourseStatus)
                    .switch(Course)
                    .join(Term).where(Term.id == termId, Course.status.status != "Approved", Course.status.status != "Completed").distinct())

    return pendingCourses

def approvedCourses(termId):
    '''
    Queries the database to get all the neccessary information for
    approved courses.
    '''

    approvedCourses = (Course.select(Course, Term)
                        .join(CourseStatus)
                        .switch(Course)
                        .join(Term).where(Term.id == termId, Course.status.status == "Approved").distinct())

    return approvedCourses

def getinstructorData(courseIds):
    """
    Gets and instructor object for the course id's given.
    """
    instructorDict = {}
    instructor = CourseInstructor.select().where(CourseInstructor.course << courseIds)

    for i in instructor:
        instructorDict.setdefault(i.course.id, []).append(i.user.firstName + " " + i.user.lastName)

    return instructorDict

def createCourse(courseData, instructorsDict):
    """This function will create a course given a form."""
    term = Term.get(Term.id==courseData["term"])
    status = CourseStatus.get(CourseStatus.status == "Pending")
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

def updateCourse(courseData, instructorsDict):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instuctors assigned to the course and update the information in the db.
    """

    for toggler in ["regularOccurenceToggle", "slSectionsToggle", "permanentDesignation"]:
        courseData.setdefault(toggler, "off")
    status = CourseStatus.get(CourseStatus.status == "Pending")
    course = Course.update(
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
        addInstructors = CourseInstructor.create(course=courseData["courseID"], user=instructor)

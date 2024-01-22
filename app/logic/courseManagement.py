from flask import flash
from peewee import fn, JOIN

from app.models import mainDB
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseQuestion import CourseQuestion
from app.models.courseStatus import CourseStatus
from app.logic.createLogs import createAdminLog
from app.logic.fileHandler import FileHandler
from app.logic.utils import getFilesFromRequest
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
                                      Course.status.in_([CourseStatus.SUBMITTED, CourseStatus.IN_PROGRESS]))
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


def importedCourses(termId):
    '''
    Queries the database to get all the necessary information for 
    imported courses.
    '''
    importedCourses = (Course.select(Course, Term, CourseStatus, fn.GROUP_CONCAT(" " ,User.firstName, " ", User.lastName).alias('instructors'))
                        .join(CourseInstructor, JOIN.LEFT_OUTER)
                        .join(User, JOIN.LEFT_OUTER).switch(Course)
                        .join(CourseStatus).switch(Course)
                        .join(Term)
                        .where(Term.id == termId, Course.status == CourseStatus.IMPORTED)
                        .group_by(Course, Term, CourseStatus))

    return importedCourses


def editImportedCourses(courseData, attachments=None):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instructors assigned to the imported course after that one is edited 
        and update the information in the db.
    """

    with mainDB.atomic() as transaction:
        try:
            course = Course.get_by_id(courseData["courseId"])
            
            (Course.update(courseName=courseData["courseName"])
                   .where(Course.id == course.id).execute()) # Update the data (Course Name) of the course in the database

            (CourseParticipant.update(hoursEarned=courseData["hoursEarned"])
                              .where(CourseParticipant.course_id == course.id).execute())
            
            instructorList = []
            if 'instructor[]' in courseData:
                instructorList = courseData.getlist('instructor[]') # Fetch the list of course instructors from CourseData
            
            if instructorList:
                CourseInstructor.delete().where(CourseInstructor.course == course).execute() # Delete existing course instructors before rolling up updates 
                for instructor in instructorList:
                    if instructor != "": # Checks that empty string is not added as a course instructor because some keys in the dictionary are empty string.
                        CourseInstructor.create(course=course, user=instructor)

            return Course.get_by_id(course.id)
        


            # # Update course table with course name
            # (Course.update(courseName=courseData["courseName"])
            #        .where(Course.id == course.id).execute()) # Update the data (Course Name) of the course in the database

            # instructorList = []
            # if 'instructor[]' in courseData:
            #     instructorList = courseData.getlist('instructor[]') # Fetch the list of course instructors from CourseData
            

            # # Update courseinstructors table
            # if instructorList:
            #     CourseInstructor.delete().where(CourseInstructor.course == course).execute() 
            #     for instructor in instructorList:
            #         if instructor != "": 
            #             CourseInstructor.create(course=course, user=instructor)

            # participantList = list(CourseParticipant.select(User).where(Course.id == course.id))


            # # Update service hours (hours earned) of participants in course participant table
            # for participant in participantList:
            #     (CourseParticipant.update(hoursEarned=courseData["hoursEarned"])
            #                       .where(Course.id == course.id, 
            #                              User == participant))

        except Exception as e:
            print(e)
            transaction.rollback()
            return False


def createCourse(creator="No user provided"):
    """ Create an empty, in progress course """
    course = Course.create(status=CourseStatus.IN_PROGRESS, createdBy=creator)
    for i in range(1, 7):
        CourseQuestion.create( course=course, questionNumber=i)

    return course

def updateCourse(courseData, attachments=None):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instructors assigned to the course and update the information in the db.
    """
    with mainDB.atomic() as transaction:
        try:
            course = Course.get_by_id(courseData['courseID'])
            for toggler in ["slSectionsToggle", "permanentDesignation"]:
                courseData.setdefault(toggler, "off")
            (Course.update(courseName=courseData["courseName"],
                           courseAbbreviation=courseData["courseAbbreviation"],
                           sectionDesignation=courseData["sectionDesignation"],
                           courseCredit=courseData["credit"],
                           isRegularlyOccurring=int(courseData["isRegularlyOccurring"]),
                           term=courseData['term'],
                           status=CourseStatus.SUBMITTED,
                           isPreviouslyApproved=int(courseData["isPreviouslyApproved"]),
                           previouslyApprovedDescription = courseData["previouslyApprovedDescription"],
                           isAllSectionsServiceLearning=("on" in courseData["slSectionsToggle"]),
                           serviceLearningDesignatedSections=courseData["slDesignation"],
                           isPermanentlyDesignated=("on" in courseData["permanentDesignation"]),
                           hasSlcComponent = int(courseData["hasSlcComponent"]))
                   .where(Course.id == course.id).execute())
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
            createAdminLog(f"Saved SLC proposal: {courseData['courseName']}")
            if attachments:
                addFile= FileHandler(attachments, courseId=course.id)
                addFile.saveFiles()
            return Course.get_by_id(course.id)
        except Exception as e:
            print(e)
            transaction.rollback()
            return False
from flask import session, g, flash
from peewee import fn, JOIN
import re as regex
from openpyxl import load_workbook

from app.models import mainDB
from app.models import DoesNotExist
from app.models.course import Course
from app.models.user import User
from app.models.term import Term
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseStatus import CourseStatus
from app.models.courseQuestion import CourseQuestion
from app.models.attachmentUpload import AttachmentUpload
from app.models.questionNote import QuestionNote
from app.models.note import Note
from app.logic.createLogs import createAdminLog
from app.logic.fileHandler import FileHandler
from app.logic.term import addPastTerm

def getServiceLearningCoursesData(user):
    """Returns dictionary with data used to populate Service-Learning proposal table"""
    courses = (Course.select(Course, Term, User, CourseStatus)
                     .join(CourseInstructor).switch()
                     .join(Term).switch()
                     .join(CourseStatus).switch()
                     .join(User)
                     .where((CourseInstructor.user==user)|(Course.createdBy==user))
                     .order_by(Course.term.desc(), Course.status))

    courseDict = {}
    for course in courses:
        courseInstructors = (CourseInstructor.select(CourseInstructor, User).join(User).where(CourseInstructor.course==course))
        faculty = [f"{instructor.user.firstName} {instructor.user.lastName}" for instructor in courseInstructors]


        courseDict[course.id] = {"id":course.id,
                                 "creator":f"{course.createdBy.firstName} {course.createdBy.lastName}",
                                 "name":course.courseName,
                                 "faculty": faculty,
                                 "term": course.term,
                                 "status": course.status.status}
    return courseDict

def parseUploadedFile(filePath):
    """
    Parse an Excel document at the given `filePath` for courses and
    course participants.

    The return value will be a tuple. The second value is a list of 
    error message tuples. The first tuple value is the error message, 
    and the second is a 0 or 1 indicating whether the error is a 
    'general' error - 1 - or an error on a specific course, term, or 
    person.  The first value is a dictionary keyed by the term 
    description. Each value is another dictionary, with a key for 
    'displayMsg' and 'errorMsg', and a 'courses' key whose value is 
    a dictionary with keys for the courses in the term. Each course 
    has a 'displayMsg' and 'errorMsg' key, and a 'students' key 
    that has a list of dictionaries with 'user', 'displayMsg', and 
    'errorMsg' keys.
    E.g.,
    {
        "Fall 2021": {
            "displayMsg": "",
            "errorMsg": "",
            "courses": {
                "CSC 330": {
                    "displayMsg: "CSC 330 will be created",
                    "errorMsg: "",
                    "students": [
                        {'user':'ramsayb2', 
                         'displayMsg': 'Brian Ramsay',
                         'errorMsg': ''},
                        {'user':'B0073235', 
                         'displayMsg': '',
                         'errorMsg': 'ERROR: B0073235 does not exist!'}]
                },
                "CSC 226": {
                    "displayMsg": "CSC 226 matched to existing course 'Data Structures'.",
                    "errorMsg": "",
                    "students": [
                        {'user':'ramsayb2', 
                         'displayMsg': 'Brian Ramsay',
                         'errorMsg': ''},
                        {'user':'lamichhanes', 
                         'displayMsg': 'Sandesh Lamichhane',
                         'errorMsg': ''}]
                }
           }
        }
    }
    """
    excelData = load_workbook(filename=filePath)
    excelSheet = excelData.active

    result= {}
    errors = []
    term = ''
    course = ''
    cellRow = 0

    for row in excelSheet.iter_rows():
        cellRow += 1
        cellVal = row[0].value
        if not cellVal:
            continue

        # Look for a Term. Examples: Fall 2020 or Spring B 2021
        if regex.search(r"\b[a-zA-Z]{3,}( [AB])? \d{4}\b", str(cellVal)):
            errorMsg = ''
            if "Spring A" in cellVal or "Spring B" in cellVal:
                cellVal = "Spring " + cellVal.split()[-1]
            if "Fall A" in cellVal or "Fall B" in cellVal:
                cellVal = "Fall " + cellVal.split()[-1]
                
            if cellVal.split()[0] not in ["Summer", "Spring", "Fall", "May"]:
                errorMsg = f"ERROR: '{cellVal}' is not a valid term in row {cellRow}."
            else:
                latestTerm = Term.select().order_by(Term.termOrder.desc()).get()
                isFutureTerm = latestTerm.termOrder < Term.convertDescriptionToTermOrder(cellVal)
                if isFutureTerm:
                    errors.append(f"ERROR: '{cellVal}' is a future term in row {cellRow}.")
                else:
                    validTerm = Term.get_or_none(Term.description == cellVal)

            term = cellVal
            result[term] = {
                'displayMsg': term,
                'errorMsg': errorMsg,
                'courses': {}
            }
            if errorMsg:
                errors.append((errorMsg,0))

        # Look for a Course. Examples: FRN134 CSC 226
        elif regex.search(r"\b[A-Z]{2,4} ?\d{3}\b", str(cellVal)):
            errorMsg = displayMsg = ''
            if not term:
                displayMsg = cellVal
                errorMsg = "ERROR: No term was given for this course"
            else:
                existingCourse = Course.get_or_none(Course.courseAbbreviation == cellVal)
                displayMsg = f'{cellVal} will be created.'
                if existingCourse:
                    displayMsg = f"{cellVal} matched to the existing course {existingCourse.courseName}."

            course = cellVal
            result[term]['courses'][course] = {
                'displayMsg': displayMsg,
                'errorMsg': errorMsg,
                'students': []
            }
            if errorMsg:
                errors.append((errorMsg,0))

        # Look for a B-Number. Example: B00123456
        elif regex.search(r"\b[B]\d{8}\b", str(cellVal)):      
            errorMsg = displayMsg = ''
            if not course:
                errorMsg = "ERROR: No course is connected to this student"
            else:
                existingUser = User.get_or_none(User.bnumber == cellVal)
                if existingUser:
                    displayMsg = f"{existingUser.firstName} {existingUser.lastName}"
                    existingUser = existingUser.username
                else:             
                    errorMsg = f'ERROR: {row[1].value} with B# "{row[0].value}" does not exist.'

            result[term]['courses'][course]['students'].append({
                'user': (existingUser or cellVal),
                'displayMsg': displayMsg,
                'errorMsg': errorMsg})
            if errorMsg:
                errors.append((errorMsg,0))
            
        elif cellVal: # but didn't match the regex
            errors.append((f'ERROR: "{cellVal}" in row {cellRow} of the Excel document does not appear to be a term, course, or valid B#.',1))
        

    return result, errors

def saveCourseParticipantsToDatabase(cpPreview):
    for term,terminfo in cpPreview.items():
        termObj = Term.get_or_none(description = term) or addPastTerm(term)
        if not termObj:
            print(f"Unable to find or create term {term}")
            continue

        for course, courseinfo in terminfo['courses'].items():
            if 'errorMsg' in courseinfo and courseinfo['errorMsg']:
                print(f"Unable to save course {course}. {courseinfo['errorMsg']}")
                continue

            courseObj = Course.get_or_create(
                 courseAbbreviation = course,
                 term = termObj, 
                 defaults = {"CourseName" : "",
                             "sectionDesignation" : "",
                             "courseCredit" : "1",
                             "term" : termObj,
                             "status" : 4,
                             "createdBy" : g.current_user,
                             "serviceLearningDesignatedSections" : "",
                             "previouslyApprovedDescription" : "" })[0]

            for userDict in courseinfo['students']:
                if userDict['errorMsg']:
                    print(f"Unable to save student. {userDict['errorMsg']}")
                    continue

                CourseParticipant.get_or_create(user=userDict['user'], 
                                                course=courseObj,
                                                hoursEarned=20)
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

def createCourse(creator="No user provided"):
    """ Create an empty, in progress course """
    course = Course.create(status=CourseStatus.IN_PROGRESS, createdBy=creator)
    for i in range(1, 7):
        CourseQuestion.create( course=course, questionNumber=i)

    return course

def updateCourse(courseData, attachments=None):
    """
        This function will take in courseData for the SLC proposal page and a dictionary
        of instuctors assigned to the course and update the information in the db.
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
        

def withdrawProposal(courseID):
    """Withdraws proposal of ID passed in. Removes foreign keys first.
    Key Dependencies: QuestionNote, CourseQuestion, CourseParticipant,
    CourseInstructor, Note"""

    # delete syllabus
    try:
        syllabi = AttachmentUpload.select().where(AttachmentUpload.course==courseID)
        for syllabus in syllabi:
            FileHandler(courseId = courseID).deleteFile(syllabus.id)

    except DoesNotExist:
        print(f"File, {AttachmentUpload.fileName}, does not exist.")

    # delete course object
    course = Course.get(Course.id == courseID)
    courseName = course.courseName
    questions = CourseQuestion.select().where(CourseQuestion.course == course)
    notes = list(Note.select(Note.id)
                     .join(QuestionNote)
                     .where(QuestionNote.question.in_(questions))
                     .distinct())
    course.delete_instance(recursive=True)
    for note in notes:
        note.delete_instance()

    createAdminLog(f"Withdrew SLC proposal: {courseName}")

def renewProposal(courseID, term):
    """
    Renews proposal of ID passed in for the selected term.
    Sets status to in progress.
    """
    oldCourse = Course.get_by_id(courseID)
    newCourse = Course.get_by_id(courseID)
    newCourse.id = None
    newCourse.term = Term.get_by_id(term)
    newCourse.status = CourseStatus.IN_PROGRESS
    newCourse.isPreviouslyApproved = True
    newCourse.save()
    questions = CourseQuestion.select().where(CourseQuestion.course==oldCourse)
    for question in questions:
        CourseQuestion.create(course=newCourse.id,
                              questionContent=question.questionContent,
                              questionNumber=question.questionNumber)

    instructors = CourseInstructor.select().where(CourseInstructor.course==oldCourse.id)
    for instructor in instructors:
        CourseInstructor.create(course=newCourse.id,
                                user=instructor.user)

    return newCourse

def getInstructorCourses():
    """
    This function selects all the Instructors Name and the previous courses
    """
    instructors = (CourseInstructor.select(CourseInstructor, User, Course)
                                   .join(User).switch()
                                   .join(Course))
    result = {}

    for instructor in instructors:
        result.setdefault(instructor.user, [])
        if instructor.course.courseName not in result[instructor.user]:
            result[instructor.user].append(instructor.course.courseName)

    return result
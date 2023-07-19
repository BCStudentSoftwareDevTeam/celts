from app.models.course import Course
from app.models.user import User
from app.models.term import Term
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseStatus import CourseStatus
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.note import Note
from app.models.attachmentUpload import AttachmentUpload
from app.models.term import Term
from app.models import DoesNotExist
from app.logic.createLogs import createAdminLog
from app.logic.fileHandler import FileHandler
from flask import flash, abort, jsonify, session, send_file, g
import re
import os
from openpyxl import load_workbook
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
        otherInstructors = (CourseInstructor.select(CourseInstructor, User).join(User).where(CourseInstructor.course==course))
        faculty = [f"{instructor.user.firstName} {instructor.user.lastName}" for instructor in otherInstructors]


        courseDict[course.id] = {
        "id":course.id,
        "creator":f"{course.createdBy.firstName} {course.createdBy.lastName}",
        "name":course.courseName,
        "faculty": faculty,
        "term": course.term,
        "status": course.status.status}
    return courseDict

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

def parseUploadedFile(filePath):
    excelData = load_workbook(filename=filePath)
    excelSheet = excelData.active
    termReg = r"\b[a-zA-Z]{3,}\s\d{4}\b" # regular expression to check cells content
    courseReg = r"\b[A-Z]{2,4}\s\d{3}\b"
    bnumberReg = r"\b[B]\d{8}\b"

    previewParticipants = []
    individualCourse = []
    listOfStudentsBnumber = []
    errorFlag = False
    termDictionary= {}
    previewTerm = ''
    previewCourse = ''
    studentValue= ''

    for row in excelSheet.iter_rows():
        cellVal = row[0].value

        if re.search(termReg, str(cellVal)):
            previewTerm = ''
            hasTerm = Term.get_or_none(Term.description == cellVal)
            if hasTerm:
                previewTerm = cellVal 
            elif list(Term.select().order_by(Term.termOrder))[-1].termOrder > Term.convertTerm(cellVal):
                previewTerm = cellVal
            else:
                previewTerm = f"ERROR: The term {cellVal} does not exist."
                errorFlag = True

            termDictionary[previewTerm]= {}

        elif re.search(courseReg, str(cellVal)):
            previewCourse = ''
            hasCourse = Course.get_or_none(Course.courseAbbreviation == cellVal)

            previewCourse = cellVal
            if hasCourse and hasCourse.courseName:
                previewCourse = hasCourse.courseName

            individualCourse = []
            individualCourse.append([previewCourse, cellVal])
            individualCourse.append(previewTerm)
            previewParticipants.append(individualCourse)
            termDictionary[previewTerm][previewCourse]=[]
           
        elif re.search(bnumberReg, str(cellVal)):      
            
            hasUser = User.get_or_none(User.bnumber == cellVal)

            if hasUser:
                individualStudent = {
                    "bnumber": hasUser.bnumber,
                    "student_name": hasUser.firstName + hasUser.lastName          
                    }
                listOfStudentsBnumber.append(individualStudent)
                studentValue =f"{hasUser.firstName} {hasUser.lastName}"
                individualCourse.append(studentValue)
                
            else:
                previewStudent = row[1].value
                individualStudent = {
                    "bnumber": f"A student with bnumber {cellVal} doesn't exist.",
                    "student_name": f"{previewStudent} does not exist."         
                    }
                listOfStudentsBnumber.append(individualStudent)
                studentValue = f"ERROR: {previewStudent} does not exist."
                individualCourse.append(studentValue)
                errorFlag = True
            termDictionary[previewTerm][previewCourse].append(studentValue)
            
    return previewParticipants, listOfStudentsBnumber, errorFlag, termDictionary

def pushDataToDatabase(listOfParticipants,listOfBnumbers):
    courseGet = None
    for courseInfo in listOfParticipants:
        termOfCourse = courseInfo[1]
        term = Term.get_or_none(description=termOfCourse) 
        if not term :
            term=addPastTerm(termOfCourse)

        courseNumber = courseInfo[0][1]
        courseGet = Course.get_or_create(courseAbbreviation = courseNumber, defaults = {
                "CourseName" : "",
                "sectionDesignation" : "",
                "courseCredit" : "1",
                "term" : term,
                "status" : 3,
                "createdBy" : g.current_user,
                "serviceLearningDesignatedSections" : "",
                "previouslyApprovedDescription" : ""
                }
            ) 
        for studentDict in listOfBnumbers:
            bnumberStudent = studentDict["bnumber"]

            user = User.get(User.bnumber == bnumberStudent)
            CourseParticipant.get_or_create(user = user, defaults = {
                "course" : courseGet[0],
                "hoursEarned" : 2
            })

def sessionCleaner():
    session.pop('dataPreview')
    session.pop('listofBnumber_students')
    session.pop('errorFlag')
    session.pop('termDict')
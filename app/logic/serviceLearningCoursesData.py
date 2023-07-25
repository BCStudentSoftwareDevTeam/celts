from flask import session, g
import re as regex
from openpyxl import load_workbook
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


        courseDict[course.id] = {"id":course.id,
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
    errorFlag = False
    courseParticipantPreview= {}
    previewTerm = ''
    previewCourse = ''
    studentValue= ''
    cellRow = 1
    previewCourseDisplayList = []
    

    for row in excelSheet.iter_rows():
        cellVal = row[0].value
        displayRow  = ''
        termReg = r"\b[a-zA-Z]{3,}\s\d{4}\b" # regular expression to check cells content
        courseReg = r"\b[A-Z]{2,4}\s\d{3}\b"
        bnumberReg = r"\b[B]\d{8}\b"

        if regex.search(termReg, str(cellVal)):
            if cellVal.split()[0] not in ["Summer", "Spring", "Fall", "May"]:
                previewTerm = f"ERROR: {cellVal} is not valid."
                errorFlag = True 
                displayRow = f"ERROR-{previewTerm}"
            else:
                previousTerm = list(Term.select().order_by(Term.termOrder))[-1].termOrder > Term.convertDescriptionToTermOrder(cellVal)
                hasTerm = Term.get_or_none(Term.description == cellVal)
                if hasTerm or previousTerm:
                    previewTerm = cellVal 
                    displayRow = f"TERM-{previewTerm}"
                else:
                    previewTerm = f"ERROR: The term {cellVal} does not exist and cannot be automatically created."
                    errorFlag = True
                    displayRow = f"ERROR-{previewTerm}"
            courseParticipantPreview[previewTerm]= {}

        elif regex.search(courseReg, str(cellVal)):
            hasCourse = Course.get_or_none(Course.courseAbbreviation == cellVal)
            previewCourse = f'{cellVal} will be created'
            if hasCourse and hasCourse.courseName:
                previewCourse = f"{cellVal} matched to the course {hasCourse.courseName}"
            if not courseParticipantPreview.get(previewTerm):
                courseParticipantPreview[previewTerm]= {}
            courseParticipantPreview[previewTerm][cellVal]=[]
            displayRow = f"COURSE-{previewCourse}"

        elif regex.search(bnumberReg, str(cellVal)):      
            hasUser = User.get_or_none(User.bnumber == cellVal)
            if hasUser:
                studentValue = f"{hasUser.firstName} {hasUser.lastName}"
                displayRow = f"STUDENT-{studentValue}"
            else:             
                studentValue = f'ERROR: {row[1].value} with B# "{row[0].value}" does not exist.'
                errorFlag = True
                displayRow = f"ERROR-{studentValue}"
            if not courseParticipantPreview.get(previewTerm):
                courseParticipantPreview[previewTerm]= {}
            if not courseParticipantPreview[previewTerm].get(previewCourse):
                courseParticipantPreview[previewTerm][previewCourse]=[]
            courseParticipantPreview[previewTerm][previewCourse].append([studentValue, cellVal])
            
        elif cellVal != '' and cellVal != None:
            errorText = f'ERROR: {cellVal} in row {cellRow} of the Excel document is not a valid value.'
            errorFlag = True
            displayRow = f"ERROR-{errorText}"
        
        if displayRow: 
            previewCourseDisplayList.append(displayRow)

        cellRow += 1

    return errorFlag, courseParticipantPreview, previewCourseDisplayList

def saveCourseParticipantsToDatabase(courseParticipantPreview):
    for term in courseParticipantPreview:
        termObj = Term.get_or_none(description = term) or addPastTerm(term)

        for course in courseParticipantPreview[term]:
            courseObj = Course.get_or_create(courseAbbreviation = course,
                                             term = termObj.id, 
                                             defaults = {"CourseName" : "",
                                                         "sectionDesignation" : "",
                                                         "courseCredit" : "1",
                                                         "term" : termObj,
                                                         "status" : 4,
                                                         "createdBy" : g.current_user,
                                                         "serviceLearningDesignatedSections" : "",
                                                         "previouslyApprovedDescription" : "" })
            
            for student, bNumber in courseParticipantPreview[term][course]:
                userObj = User.get(User.bnumber == bNumber)
                CourseParticipant.get_or_create(user = userObj,
                                                course = courseObj[0],
                                                defaults = {"course" : courseObj[0]})


def courseParticipantPreviewSessionCleaner():
    session.pop('errorFlag')
    session.pop('courseParticipantPreview')
    session.pop('previewCourseDisplayList')
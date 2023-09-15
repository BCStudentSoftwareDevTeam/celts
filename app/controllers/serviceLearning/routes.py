from flask import request, render_template, g, url_for, abort, redirect, flash, session, send_from_directory, send_file, jsonify
from werkzeug.utils import safe_join
import os
from peewee import *
from app.models.user import User
from app.models.term import Term
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.attachmentUpload import AttachmentUpload
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.fileHandler import FileHandler
from app.logic.serviceLearningCoursesData import getServiceLearningCoursesData, withdrawProposal, renewProposal
from app.logic.courseManagement import updateCourse, createCourse
from app.logic.downloadFile import *
from app.logic.courseManagement import approvedCourses
from app.logic.utils import getRedirectTarget, setRedirectTarget
from app.controllers.serviceLearning import serviceLearning_bp


@serviceLearning_bp.route('/serviceLearning/courseManagement', methods = ['GET'])
@serviceLearning_bp.route('/serviceLearning/courseManagement/<username>', methods = ['GET'])
def serviceCourseManagement(username=None):
    try:
        user = User.get(User.username==username) if username else g.current_user
    except DoesNotExist:
        abort(404)
    
    isRequestingForSelf = g.current_user == user 
    if g.current_user.isCeltsAdmin or (g.current_user.isFaculty and isRequestingForSelf):
        setRedirectTarget(request.full_path)
        courseDict = getServiceLearningCoursesData(user)
        termList = selectSurroundingTerms(g.current_term, prevTerms=0)
        return render_template('serviceLearning/slcManagement.html',
            user=user,
            courseDict=courseDict,
            termList=termList)
    else:
        abort(403)
        

@serviceLearning_bp.route('/serviceLearning/viewProposal/<courseID>', methods=['GET'])
@serviceLearning_bp.route('/serviceLearning/editProposal/upload/<courseID>', methods=['GET'])
@serviceLearning_bp.route('/serviceLearning/editProposal/<courseID>', methods=['GET'])
def slcEditProposal(courseID):
    """
        Route for editing proposals, it will fill the form with the data found in the database
        given a courseID.
    """
    instructors = CourseInstructor.select().where(CourseInstructor.course==courseID)
    courseInstructors = [instructor.user for instructor in instructors]
    isCourseCreator = Course.select().where(Course.createdBy == g.current_user, Course.id==courseID).exists()

    if g.current_user.isCeltsAdmin or g.current_user in courseInstructors or isCourseCreator:
        course = Course.get_by_id(courseID)
        courseStatus = CourseStatus.get_by_id(course.status)
        courseStatusInt = courseStatus.get_id()
        approved = 3
        # Condition to check the route you are comming from
        if courseStatusInt==approved and request.path == f"/serviceLearning/editProposal/{courseID}":
            return redirect(f"/serviceLearning/viewProposal/{courseID}")
        else:
            statusOfCourse = Course.select(Course.status)
            questionData = (CourseQuestion.select().where(CourseQuestion.course == course))
            questionanswers = [question.questionContent for question in questionData]
            courseInstructor = CourseInstructor.select().where(CourseInstructor.course == courseID)
            associatedAttachments = AttachmentUpload.select().where(AttachmentUpload.course == course.id)

            filepaths = FileHandler(courseId=course.id).retrievePath(associatedAttachments)

            terms = selectSurroundingTerms(g.current_term, 0)
            return render_template('serviceLearning/slcNewProposal.html',
                                        course = course,
                                        questionanswers = questionanswers,
                                        terms = terms,
                                        statusOfCourse = statusOfCourse,
                                        courseStatus = courseStatus,
                                        courseInstructor = courseInstructor,
                                        filepaths = filepaths,
                                        redirectTarget=getRedirectTarget())
    else:
        abort(403)
        

@serviceLearning_bp.route('/serviceLearning/createCourse', methods=['POST'])
def slcCreateCourse():
    """will give a new course ID so that it can redirect to an edit page"""
    course = createCourse(g.current_user)

    return redirect(url_for('serviceLearning.slcEditProposal', courseID = course.id))


@serviceLearning_bp.route('/serviceLearning/exit', methods=['GET'])
def slcExitView():
    if getRedirectTarget():
        return redirect(getRedirectTarget(True))
    else:
        return redirect("/serviceLearning/courseManagement")


@serviceLearning_bp.route('/serviceLearning/saveExit', methods=['POST'])
@serviceLearning_bp.route('/serviceLearning/saveProposal', methods=['POST'])
def slcSaveContinue():
    """Will update the the course proposal and return an empty string since ajax request needs a response
    Also, it updates the course status as 'in progress'"""
    course = updateCourse(request.form.copy(), attachments=getFilesFromRequest(request))

    if not course:
        flash("Error saving changes", "danger")
    else:
        course.status = CourseStatus.IN_PROGRESS
        course.save()
        flash(f"Proposal has been saved.", "success")
    if request.path == "/serviceLearning/saveExit":
        if getRedirectTarget():
            return redirect(getRedirectTarget(True))
        return redirect("/serviceLearning/courseManagement")
    return redirect(f'/serviceLearning/editProposal/{request.form["courseID"]}?tab=2')

@serviceLearning_bp.route('/serviceLearning/newProposal', methods=['GET', 'POST'])
def slcCreateOrEdit():
    if request.method == "POST":
        course = updateCourse(request.form.copy())
        if not course:
            flash("Error saving changes", "danger")
        else:
            if getRedirectTarget(False):
                return redirect('' + getRedirectTarget(True) + '')
            return redirect('/serviceLearning/courseManagement')

    terms = Term.select().where(Term.year >= g.current_term.year)
    courseData = None
    return render_template('serviceLearning/slcNewProposal.html',
                terms = terms,
                courseData = courseData,
                redirectTarget = getRedirectTarget(True))

@serviceLearning_bp.route('/serviceLearning/approveCourse', methods=['POST'])
def approveCourse():
    """
    This function updates and approves a Service-Learning Course when using  the
        approve button.
    return: empty string because AJAX needs to receive something
    """

    try:
        # We are only approving, and not updating
        if len(request.form) == 1:
            course = Course.get_by_id(request.form['courseID'])

        # We have data and need to update the course first
        else:
            course = updateCourse(request.form.copy())

        course.status = CourseStatus.APPROVED
        course.save()
        flash("Course approved!", "success")

    except Exception as e:
        print(e)
        flash("Course not approved!", "danger")
    return ""
@serviceLearning_bp.route('/serviceLearning/unapproveCourse', methods=['POST'])
def unapproveCourse():
    """
    This function updates and unapproves a Service-Learning Course when using the
        unapprove button.
    return: empty string because AJAX needs to receive something
    """

    try:
        if len(request.form) == 1:
            course = Course.get_by_id(request.form['courseID'])
        else:
            course = updateCourse(request.form.copy())

        course.status = CourseStatus.SUBMITTED
        course.save()
        flash("Course unapproved!", "success")

    except Exception as e:
        print(e)
        flash("Course was not unapproved!", "danger")

    return ""

@serviceLearning_bp.route('/updateInstructorPhone', methods=['POST'])
def updateInstructorPhone():
    instructorData = request.get_json()
    (User.update(phoneNumber=instructorData[1])
        .where(User.username == instructorData[0])).execute()
    return "success"

@serviceLearning_bp.route('/serviceLearning/withdraw/<courseID>', methods = ['POST'])
def withdrawCourse(courseID):
    try:
        if g.current_user.isAdmin or g.current_user.isFaculty:
            withdrawProposal(courseID)
            flash("Course successfully withdrawn", 'success')
        else:
            flash("Unauthorized to perform this action", 'warning')
    except Exception as e:
        print(e)
        flash("Withdrawal Unsuccessful", 'warning')
    return ""

@serviceLearning_bp.route('/serviceLearning/renew/<courseID>/<termID>/', methods = ['POST'])
def renewCourse(courseID, termID):
    """
    This function checks to see if the user is a CELTS admin or is
        an instructor of a course (faculty) and allows courses to be renewed.
    :return: empty string because AJAX needs to receive something
    """
    instructors = CourseInstructor.select().where(CourseInstructor.course==courseID)
    courseInstructors = [instructor.user for instructor in instructors]
    isCourseCreator = Course.select().where(Course.createdBy == g.current_user, Course.id==courseID).exists()
    try:
        if g.current_user.isCeltsAdmin or g.current_user in courseInstructors or isCourseCreator:
            renewedProposal = renewProposal(courseID, termID)
            flash("Course successfully renewed", 'success')
            return str(renewedProposal.id)
        else:
            flash("Unauthorized to perform this action", 'warning')
    except Exception as e:
        print(e)
        flash("Renewal Unsuccessful", 'warning')

    return "", 500

@serviceLearning_bp.route('/serviceLearning/print/<courseID>', methods=['GET'])
def printCourse(courseID):
    """
    This function will print a PDF of an SLC proposal.
    """
    instructors = CourseInstructor.select().where(CourseInstructor.course==courseID)
    courseInstructors = [instructor.user for instructor in instructors]
    isCreator = Course.select().where(Course.createdBy == g.current_user, Course.id==courseID).exists()
    if g.current_user.isCeltsAdmin or g.current_user in courseInstructors or isCreator:
        try:
            course = Course.get_by_id(courseID)
            pdfCourse = Course.select().where(Course.id == courseID)
            pdfInstructor = CourseInstructor.select().where(CourseInstructor.course == courseID)
            pdfQuestions = (CourseQuestion.select().where(CourseQuestion.course == course))
            questionanswers = [question.questionContent for question in pdfQuestions]

            return render_template('serviceLearning/slcFormPrint.html',
                                    course = course,
                                    pdfCourse = pdfCourse,
                                    pdfInstructor = pdfInstructor,
                                    pdfQuestions = pdfQuestions,
                                    questionanswers=questionanswers
                                    )
        except Exception as e:
            flash("An error was encountered when printing, please try again.", 'warning')
            print(e)
            return "", 500
    else:
        abort(403)

@serviceLearning_bp.route("/uploadCourseFile", methods=['GET', "POST"])
def uploadCourseFile():
    try:
        attachment = getFilesFromRequest(request)
        courseID = request.form["courseID"]
        addFile= FileHandler(attachment, courseId=courseID)
        addFile.saveFiles()
    except:
        flash("No file selected.", "warning")
    return redirect('/serviceLearning/editProposal/upload/'+courseID)


@serviceLearning_bp.route("/deleteCourseFile", methods=["POST"])
def deleteCourseFile():
    fileData= request.form
    courseFile=FileHandler(courseId=fileData["databaseId"])
    courseFile.deleteFile(fileData["fileId"])
    return ""

@serviceLearning_bp.route('/serviceLearning/downloadApprovedCourses/<termID>', methods = ['GET'])
def downloadApprovedCourses(termID):
    """
    This function allows the download of csv file
    """
    try:
        designator = "downloadApprovedCourses"
        csvInfo = approvedCourses(termID)
        fileFormat = {"headers":["Course Name", "Course Number", "Faculty", "Term", "Previously Approved Course?"]}
        filePath = safe_join(os.getcwd(), app.config['files']['base_path'])
        newFile = fileMaker(designator, csvInfo, "CSV", fileFormat)
        return send_from_directory(filePath, 'ApprovedCourses.csv', as_attachment=True)

    except Exception as e:
        print(e)
        return ""

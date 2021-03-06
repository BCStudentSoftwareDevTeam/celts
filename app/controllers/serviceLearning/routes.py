from flask import request, render_template, g, abort, json, redirect, jsonify, flash, session
from app.models.user import User
from app.models.term import Term
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.courseParticipant import CourseParticipant
from app.logic.utils import selectSurroundingTerms
from app.logic.searchUsers import searchUsers
from app.logic.utils import selectSurroundingTerms
from app.logic.serviceLearningCoursesData import getServiceLearningCoursesData, withdrawProposal, renewProposal
from app.logic.courseManagement import updateCourse, createCourse
from app.controllers.main.routes import getRedirectTarget, setRedirectTarget
from app.controllers.serviceLearning import serviceLearning_bp


@serviceLearning_bp.route('/serviceLearning/courseManagement', methods = ['GET'])
@serviceLearning_bp.route('/serviceLearning/courseManagement/<username>', methods = ['GET'])
def serviceCourseManagement(username=None):
    """This is a Temporary Page for the Service Course Management Screen."""
    # TODO: How to make accessing other user's interfaces more userfriendly?
    if g.current_user.isStudent:
        abort(403)
    if g.current_user.isCeltsAdmin or g.current_user.isFaculty:
        setRedirectTarget("/serviceLearning/courseManagement")
        user = User.get(User.username==username) if username else g.current_user
        courseDict = getServiceLearningCoursesData(user)
        termList = selectSurroundingTerms(g.current_term, prevTerms=0)
        return render_template('serviceLearning/slcManagement.html',
            user=user,
            courseDict=courseDict,
            termList=termList)
    else:
        flash("Unauthorized to view page", 'warning')
        return redirect(url_for('main.events', selectedTerm=g.current_term))

@serviceLearning_bp.route('/serviceLearning/viewProposal/<courseID>', methods=['GET'])
@serviceLearning_bp.route('/serviceLearning/editProposal/<courseID>', methods=['GET', 'POST'])
def slcEditProposal(courseID):
    """
        Route for editing proposals, it will fill the form with the data found in the database
        given a courseID.
    """
    questionData = CourseQuestion.select().where(CourseQuestion.course == courseID)
    questionanswers = [question.questionContent for question in questionData]
    courseData = questionData[0]
    courseInstructor = CourseInstructor.select().where(CourseInstructor.course == courseID)

    isRegularlyOccuring = ""
    isAllSectionsServiceLearning = ""
    isPermanentlyDesignated = ""

    if courseData.course.isRegularlyOccuring:
        isRegularlyOccuring = True
    if courseData.course.isAllSectionsServiceLearning:
        isAllSectionsServiceLearning = True
    if courseData.course.isPermanentlyDesignated:
        isPermanentlyDesignated = True
    terms = selectSurroundingTerms(g.current_term, 0)
    return render_template('serviceLearning/slcNewProposal.html',
                                courseData = courseData,
                                questionanswers = questionanswers,
                                terms = terms,
                                courseInstructor = courseInstructor,
                                isRegularlyOccuring = isRegularlyOccuring,
                                isAllSectionsServiceLearning = isAllSectionsServiceLearning,
                                isPermanentlyDesignated = isPermanentlyDesignated,
                                courseID=courseID,
                                redirectTarget = getRedirectTarget(True))

@serviceLearning_bp.route('/serviceLearning/newProposal', methods=['GET', 'POST'])
def slcCreateOrEdit():
    if request.method == "POST":
        courseExist = Course.get_or_none(Course.id == request.form.get('courseID'))
        if courseExist:
            updateCourse(request.form.copy())
        else:
            createCourse(request.form.copy(), g.current_user)
        if getRedirectTarget(False):
            return redirect('' + getRedirectTarget(True) + '')
        return redirect('/serviceLearning/courseManagement')
    terms = Term.select().where(Term.year >= g.current_term.year)
    courseData = None
    return render_template('serviceLearning/slcNewProposal.html', 
                terms = terms, 
                courseData = courseData, 
                redirectTarget = getRedirectTarget(True))

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

    try:
        if g.current_user.isCeltsAdmin or g.current_user in courseInstructors:
            renewProposal(courseID, termID)
            flash("Course successfully renewed", 'success')
        else:
            flash("Unauthorized to perform this action", 'warning')
    except Exception as e:
        print(e)
        flash("Renewal Unsuccessful", 'warning')
    return ""

@serviceLearning_bp.route('/serviceLearning/approveCourse/', methods=['POST'])
def approveCourse():
    """
    This function updates and approves a Service-Learning Course when using  the
        approve button.
    return: empty string because AJAX needs to receive something
    """
    if len(request.form) == 1:
        course = Course.get_by_id(request.form['courseID']) # if only course is reviewed pass the course ID

    elif 'courseID' in request.form:
        course = updateCourse(request.form.copy()) # if edit course, Updates database with the completed fields and get course ID
    else:
        course = createCourse(request.form.copy(), g.current_user) # creat course first and get its ID to approve next
    try:
        course.status = CourseStatus.APPROVED
        course.save() # saves the query and approves course in the database
        flash("Course approved!", "success")
    except:
        flash("Course not approved!", "danger")
    return ""

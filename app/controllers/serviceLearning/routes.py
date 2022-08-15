from flask import request, render_template, g, url_for, abort, redirect, flash, session
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
@serviceLearning_bp.route('/serviceLearning/editProposal/<courseID>', methods=['GET'])
def slcEditProposal(courseID):
    """
        Route for editing proposals, it will fill the form with the data found in the database
        given a courseID.
    """
    course = Course.get_by_id(courseID)
    questionData = (CourseQuestion.select().where(CourseQuestion.course == course))
    questionanswers = [question.questionContent for question in questionData]
    courseInstructor = CourseInstructor.select().where(CourseInstructor.course == courseID)

    isAllSectionsServiceLearning = ""
    isPermanentlyDesignated = ""

    if course.isAllSectionsServiceLearning:
        isAllSectionsServiceLearning = True
    if course.isPermanentlyDesignated:
        isPermanentlyDesignated = True
    terms = selectSurroundingTerms(g.current_term, 0)
    return render_template('serviceLearning/slcNewProposal.html',
                                course = course,
                                questionanswers = questionanswers,
                                terms = terms,
                                courseInstructor = courseInstructor,
                                isAllSectionsServiceLearning = isAllSectionsServiceLearning,
                                isPermanentlyDesignated = isPermanentlyDesignated,
                                redirectTarget=getRedirectTarget())

@serviceLearning_bp.route('/serviceLearning/createCourse', methods=['POST'])
def slcCreateCourse():
    """will give a new course ID so that it can redirect to an edit page"""
    course = createCourse(g.current_user)

    return redirect(url_for('serviceLearning.slcEditProposal', courseID = course.id))


@serviceLearning_bp.route('/serviceLearning/saveProposal', methods=['POST'])
def slcSaveContinue():
    """Will update the the course proposal and return an empty string since ajax request needs a response
    Also, it updates the course status as 'Incomplete'"""
    course = updateCourse(request.form.copy())
    course.status = CourseStatus.INCOMPLETE
    course.save()

    return ""

@serviceLearning_bp.route('/serviceLearning/newProposal', methods=['GET', 'POST'])
def slcCreateOrEdit():
    if request.method == "POST":
        course = updateCourse(request.form.copy())
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
            renewedProposal = renewProposal(courseID, termID)
            flash("Course successfully renewed", 'success')
            return str(renewedProposal.id)
        else:
            flash("Unauthorized to perform this action", 'warning')
    except Exception as e:
        print(e)
        flash("Renewal Unsuccessful", 'warning')

    return "", 500

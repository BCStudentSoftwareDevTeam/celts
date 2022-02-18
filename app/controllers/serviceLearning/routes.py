from flask import request, render_template, g, abort, json, redirect, jsonify, flash

from app.models.user import User
from app.models.term import Term
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion
from app.models.courseParticipant import CourseParticipant

from app.controllers.serviceLearning import serviceLearning_bp
from app.logic.searchUsers import searchUsers
from app.logic.serviceLearningCoursesData import getServiceLearningCoursesData, withdrawProposal
from app.logic.courseManagement import updatecourse

@serviceLearning_bp.route('/serviceLearning/courseManagement', methods = ['GET'])
@serviceLearning_bp.route('/serviceLearning/courseManagement/<username>', methods = ['GET'])
def serviceCourseManagement(username=None):
    """This is a Temporary Page for the Service Course Managment Screen."""
    # TODO: How to make accessing other user's interfaces more userfriendly?
    if g.current_user.isAdmin or g.current_user.isFaculty:
        user = User.get(User.username==username) if username else g.current_user
        courseDict = getServiceLearningCoursesData(user)
        return render_template('serviceLearning/slcManagment.html',
            user=user,
            courseDict=courseDict)
    else:
        flash("Unauthorized to view page", 'warning')
        return redirect(url_for('main.events'))

@serviceLearning_bp.route('/serviceLearning/editProposal/<courseID>', methods=['GET', 'POST'])
def slcEditProposal(courseID):
    questionData = CourseQuestion.select().where(CourseQuestion.course == courseID)
    questionanswers = [question.questionContent for question in questionData]
    courseData = questionData[0]
    courseInstructor = CourseInstructor.select().where(CourseInstructor.course == courseID)

    isRegularlyOccuring = ""
    isAllSectionsServiceLearning = ""
    isPermanentlyDesignated = ""

    if courseData.course.isRegularlyOccuring:
        isRegularlyOccuring = "checked"
    if courseData.course.isAllSectionsServiceLearning:
        isAllSectionsServiceLearning = "checked"
    if courseData.course.isPermanentlyDesignated:
        isPermanentlyDesignated = "checked"

    terms = Term.select().where(Term.year >= g.current_term.year)

    return render_template('serviceLearning/slcNewProposal.html',
                                courseData = courseData,
                                questionanswers = questionanswers,
                                terms = terms,
                                courseInstructor = courseInstructor,
                                isRegularlyOccuring = isRegularlyOccuring,
                                isAllSectionsServiceLearning = isAllSectionsServiceLearning,
                                isPermanentlyDesignated = isPermanentlyDesignated)

@serviceLearning_bp.route('/serviceLearning/newProposal', methods=['GET', 'POST'])
def slcNewProposal():
    if request.method == "POST":
        # TODO: Where to save the phone number?
        # courseData["courseInstructorPhone"] = request.form.get("courseInstructorPhone")
        term = Term.get(Term.id==request.form.get("term"))
        status = CourseStatus.get(CourseStatus.status == "Pending")
        coursecheck = Course.get_or_none(Course.courseName == request.form.get("courseName"))
        print("OVERHEREEEEEE", coursecheck)
        if coursecheck == None:
            course = Course.create(
                courseName=request.form.get("courseName"),
                courseAbbreviation=request.form.get("courseAbbreviation"),
                courseCredit=request.form.get("credit"),
                isRegularlyOccuring=1 if request.form.get("regularOccurenceToggle") else 0,
                term=term,
                status=status,
                createdBy=g.current_user,
                isAllSectionsServiceLearning=1 if request.form.get("slSectionsToggle") else 0,
                serviceLearningDesignatedSections=request.form.get("slDesignation"),
                isPermanentlyDesignated=1 if request.form.get("permanentDesignation") else 0,
            )
            for i in range(1, 7):
                CourseQuestion.create(
                    course=course,
                    questionContent=request.form.get(f"{i}"),
                    questionNumber=i
                )
            for instructor in instructorsDict["instructors"]:
                CourseInstructor.create(course=course, user=instructor.username)
            return redirect('/serviceLearning/courseManagement')
        else:
            updatecourse(request.form.copy())

    terms = Term.select().where(Term.year >= g.current_term.year)
    courseData = None
    return render_template('serviceLearning/slcNewProposal.html', terms=terms, courseData = courseData)

instructorsDict = {}
@serviceLearning_bp.route('/courseInstructors', methods=['POST'])
def getInstructors():
    instructorObjectList = []
    instructorsList = request.get_json()
    for rawInstructor in instructorsList:
        if rawInstructor != "":
            username = rawInstructor.strip("()").split('(')[-1]
            instructor = User.get(User.username==username)
            instructorObjectList.append(instructor)
    instructorsDict["instructors"] = instructorObjectList
    return jsonify({"Success": True}), 200

@serviceLearning_bp.route('/serviceLearning/withdraw/<courseID>', methods = ['POST'])
def withdrawCourse(courseID):
    try:
        if g.current_user.isAdmin or g.current_user.isFaculty:
            withdrawProposal(courseID)
            flash("Course successfully withdrawn", 'success')
        else:
            flash("Unauthorized to perform this action", 'warning')
    except Exception as e:
        flash("Withdrawal Unsuccessful", 'warning')
    return "" 

from flask import request, render_template, g, abort, json, redirect, jsonify

from app.models.user import User
from app.models.term import Term
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.courseQuestion import CourseQuestion

from app.controllers.serviceLearning import serviceLearning_bp
from app.logic.searchUsers import searchUsers

courseData = {}

@serviceLearning_bp.route('/serviceCourseManagement', methods = ['GET'])
def serviceCourseManagement():
    """This is a Temporary Page for the Service Course Managment Screen."""
    print("Landed!!")

    # TODO: Consolidate this with the controller that populates /courseProposal
    return render_template('serviceLearning/serviceCourseManagment.html', title="Welcome to CELTS!")

# TODO: Check if these three can be combined into one function?
@serviceLearning_bp.route('/slcGuidelines')
def slcGuidelines():
    """ This page renders slc guidelines """
    return render_template('serviceLearning/slcGuidelines.html')

@serviceLearning_bp.route('/slcProposal', methods=['GET', 'POST'])
def slcProposal():
    """This page allows faculties to create service learning proposal"""
    if request.method == "POST":
        courseData["courseName"] = request.form.get("courseName")
        courseData["courseAbbreviation"] = request.form.get("courseAbbreviation")
        courseData["courseCredit"] = request.form.get("credit")
        courseData["courseInstructorPhone"] = request.form.get("courseInstructorPhone")
        courseData["regularOccurenceToggle"] = request.form.get("regularOccurenceToggle")
        courseData["termId"] = request.form.get("term")
        courseData["slSectionsToggle"] = request.form.get("slSectionsToggle")
        courseData["slDesignation"] = request.form.get("slDesignation")
        courseData["permanentDesignation"] = request.form.get("permanentDesignation")
        return redirect("/slcQuestionnaire")

    terms = Term.select()
    return render_template('serviceLearning/slcProposal.html', terms=terms)

@serviceLearning_bp.route('/slcQuestionnaire', methods=['GET', 'POST'])
def slcQuestionnaire():
    """ This page renders slc questionnare """
    if request.method == "POST":
        term = Term.get(Term.id == courseData["termId"])
        status = CourseStatus.get(CourseStatus.status == "Pending")
        course = Course.create(
            courseName=courseData["courseName"],
            courseAbbreviation=courseData["courseAbbreviation"],
            courseCredit=courseData["courseCredit"],
            isRegularlyOccuring=1 if courseData["regularOccurenceToggle"] else 0,
            term=term,
            status=status,
            createdBy=g.current_user,
            isAllSectionsServiceLearning=1 if courseData["slSectionsToggle"] else 0,
            serviceLearningDesignatedSections=courseData["slDesignation"],
            isPermanentlyDesignated=1 if courseData["slDesignation"] else 0,
        )
        for i in range(1, 7):
            CourseQuestion.create(
                course=course,
                questionContent=request.form.get(f"{i}"),
                questionNumber=i
            )
        for instructor in courseData["instructors"]:
            CourseInstructor.create(course=course, user=instructor.username)
        return redirect('/serviceCourseManagement')

    return render_template('serviceLearning/slcQuestionnaire.html')

@serviceLearning_bp.route('/courseInstructors', methods=['POST'])
def getInstructors():
    instructorObjectList = []
    instructorsList = request.get_json()
    for instructor in instructorsList:
        if instructor != "":
            instructor = instructor.strip("()")
            username = instructor.split('(')[-1]
            instructor = User.get(User.username==username)
            instructorObjectList.append(instructor)
    courseData["instructors"] = instructorObjectList
    return jsonify({"Success": True}), 200

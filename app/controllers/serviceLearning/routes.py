from flask import request, render_template, g, abort, json, redirect, jsonify

from app.models.user import User
from app.models.term import Term
from app.models.course import Course
from app.models.courseStatus import CourseStatus

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
            sectionBQuestion1=request.form.get("questionOne"),
            sectionBQuestion2=request.form.get("questionTwo"),
            sectionBQuestion3=request.form.get("questionThree"),
            sectionBQuestion4=request.form.get("questionFour"),
            sectionBQuestion5=request.form.get("questionFive"),
            sectionBQuestion6=request.form.get("questionSix"),
        )
        # for instructor in courseData["instructors"]:
            # courseInstructo.create(course=course, instructor=instructor)
        return redirect('/serviceCourseManagement')

    return render_template('serviceLearning/slcQuestionnaire.html')

@serviceLearning_bp.route('/courseInstructors', methods=['POST'])
def getInstructors():
    # create new list
    # for instructor in instructorsList:
    #   # volunteer = volunteer.strip("()")
        # username = volunteer.split('(')[-1]
        # instructor = User.get(..)
        # new_list.append(instructor)
    # courseData[...] = new_list
    instructorsList = request.data.decode("utf-8")
    courseData["instructors"] = instructorsList
    return jsonify({"Success": True}), 200

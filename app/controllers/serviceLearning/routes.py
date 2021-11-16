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
from app.logic.getServiceLearningCoursesData import getServiceLearningCoursesData

@serviceLearning_bp.route('/serviceLearning/courseManagement', methods = ['GET'])
def serviceCourseManagement():
    """This is a Temporary Page for the Service Course Managment Screen."""
    courseDict = getServiceLearningCoursesData(g.current_user)
    return render_template('serviceLearning/slcManagment.html',
        instructor=g.current_user,
        courseDict=courseDict)

@serviceLearning_bp.route('/serviceLearning/newProposal', methods=['GET', 'POST'])
def slcNewProposal():
    if request.method == "POST":
        # TODO: Whose phone number will this be if there are multiple instructors?
        # courseData["courseInstructorPhone"] = request.form.get("courseInstructorPhone")
        term = Term.get(Term.id==request.form.get("term"))
        status = CourseStatus.get(CourseStatus.status == "Pending")
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

    # TODO: should it be more specific? Like filter by Fall, Spring, etc?
    terms = Term.select().where(Term.year >= g.current_term.year)
    return render_template('serviceLearning/slcNewProposal.html', terms=terms)

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

# TODO: doesnt work. Combine with the work that has already been done.
@serviceLearning_bp.route('/withdrawCourse/<courseID>', methods = ['POST'])
def withdrawCourse(courseID):
    course = Course.get(Course.id == courseID)
    (CourseInstructor.delete().where(CourseInstructor.course == course)).execute()  #need to delete all ForeignKeyFields first
    (CourseParticipant.delete().where(CourseParticipant.course == course)).execute()
    course.delete_instance()
    flash("Course successfully withdrawn", 'success')
    return "Course successfully withdrawn"

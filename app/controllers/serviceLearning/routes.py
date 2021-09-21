from flask import request, render_template, g, abort, json

from app.models.user import User
from app.models.term import Term

from app.controllers.serviceLearning import serviceLearning_bp
from app.logic.searchUsers import searchUsers

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
        courseName = request.form.get("courseName")
        courseAbbreviation = request.form.get("courseAbbreviation")
        credit = request.form.get("credit")
        courseInstructorPhone = request.form.get("courseInstructorPhone")
        regularOccurenceToggle = request.form.get("regularOccurenceToggle")
        inputCourseInstructor = request.form.get("termSelect")
        slSectionsToggle = request.form.get("slSectionsToggle")
        slDesignation = request.form.get("slDesignation")
        permanentDesignation = request.form.get("permanentDesignation")

    terms = Term.select()
    return render_template('serviceLearning/slcProposal.html', terms=terms)

@serviceLearning_bp.route('/slcQuestionnaire', methods=['GET', 'POST'])
def slcQuestionnaire():
    """ This page renders slc questionnare """
    if request.method == "POST":
        questionOne = request.form.get("questionOne")
        questionTwo = request.form.get("questionTwo")
        questionThree = request.form.get("questionThree")
        questionFour = request.form.get("questionFour")
        questionFive = request.form.get("questionFive")
        questionSix = request.form.get("questionSix")

    return render_template('serviceLearning/slcQuestionnaire.html')

@serviceLearning_bp.route('/slcSubmit', methods = ['POST'])
def slcSubmit():
    ''''''
    print("something")

# JUNK

@serviceLearning_bp.route('/searchInstructor/<query>', methods = ['GET'])
def searchInstructor(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    # TODO:
    # 1. Populate the course instructor using searchUser in logic. See if you can do it using html <form> instead of ajax.

    return json.dumps(searchUsers(query))

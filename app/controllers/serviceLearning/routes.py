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

@serviceLearning_bp.route('/slcProposal')
def slcProposal():
    """This page allows faculties to create service learning proposal"""
    terms = Term.select()
    return render_template('serviceLearning/slcProposal.html', terms=terms)

@serviceLearning_bp.route('/slcQuestionnaire')
def slcQuestionnaire():
    """ This page renders slc questionnare """
    return render_template('serviceLearning/slcQuestionnaire.html')

@serviceLearning_bp.route('/searchInstructor/<query>', methods = ['GET'])
def searchInstructor(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    # TODO:
    # 1. Populate the course instructor using searchUser in logic. See if you can do it using html <form> instead of ajax. 

    return json.dumps(searchUsers(query))

@serviceLearning_bp.route('/slcSubmit', methods = ['POST'])
def slcSubmit():
    ''''''
    print("something")

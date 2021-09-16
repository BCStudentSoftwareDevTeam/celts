from flask import request, render_template, g, abort, json
from app.controllers.serviceLearning import serviceLearning_bp
from app.models.user import User
from app.models.term import Term

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
    # TODO Items:
     # 1. Populate the course instructor (might have to wait for Sreynit and Liberty's PR to be merged)
     # 2. Populate the term
    terms = Term.select();
    return render_template('serviceLearning/slcProposal.html', terms=terms)

@serviceLearning_bp.route('/slcQuestionnaire')
def slcQuestionnaire():
    """ This page renders slc questionnare """
    return render_template('serviceLearning/slcQuestionnaire.html')

@serviceLearning_bp.route('/searchInstructor/<query>', methods = ['GET'])
def searchInstructor(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    # TODO: Liberty and Sreynit are working on consolodating search queries.
    # We could most likely use that (once merged) instead of creating a new
    # search mechanism for instructor.

    try:
        query = query.strip()
        search = query.upper() + "%"
        results = User.select().where(User.isFaculty & User.firstName ** search | User.lastName ** search)
        resultsDict = {}
        for participant in results:
            resultsDict[participant.firstName + " " + participant.lastName] = participant.firstName + " " + participant.lastName
        dictToJSON = json.dumps(resultsDict)
        return dictToJSON
    except Exception as e:
        print(e)
        return "Error Searching Instructor query", 500

@serviceLearning_bp.route('/slcSubmit', methods = ['POST'])
def slcSubmit():
    ''''''
    print("something")

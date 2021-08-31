from flask import request, render_template, g, abort, json
from app.controllers.serviceLearning import serviceLearning_bp
from app.models.user import User


@serviceLearning_bp.route('/slcProposal')
def slcProposal():
    """This page allows faculties to create service learning proposal"""

    return render_template('serviceLearning/slcProposal.html')

@serviceLearning_bp.route('/searchInstructor/<query>', methods = ['GET'])
def searchInstructor(query):
    '''Accepts user input and queries the database returning results that matches user search'''

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

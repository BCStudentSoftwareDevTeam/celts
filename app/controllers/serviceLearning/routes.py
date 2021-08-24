from flask import request, render_template, g, abort
from app.controllers.serviceLearning import serviceLearning_bp


@serviceLearning_bp.route('/serviceCourseManagement', methods = ['GET'])
def serviceCourseManagement():
    """This is a Temporary Page for the Service Course Managment Screen."""
    print("Landed!!")

    return render_template('serviceLearning/serviceCourseManagment.html', title="Welcome to CELTS!")

@serviceLearning_bp.route('/slcGuidelines')
def slcGuidelines():
    """This page display guildlines for creating service learning proposals"""

    return render_template('serviceLearning/slcGuidelines.html')

@serviceLearning_bp.route('/slcProposal')
def slcProposal():
    """This page allows faculties to create service learning proposal"""

    return render_template('serviceLearning/slcProposal.html')

@serviceLearning_bp.route('/slcQuestionnaire')
def slcQuestionnaire():
    """This page requires faculties to answering questions regarding service learning proposal"""

    return render_template('serviceLearning/slcQuestionnaire.html')

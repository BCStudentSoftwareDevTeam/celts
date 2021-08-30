from flask import request, render_template, g, abort
from app.controllers.serviceLearning import serviceLearning_bp


@serviceLearning_bp.route('/slcProposal')
def slcProposal():
    """This page allows faculties to create service learning proposal"""

    return render_template('serviceLearning/slcProposal.html')

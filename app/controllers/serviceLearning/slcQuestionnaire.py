from flask import request, render_template, g, abort
from app.controllers.serviceLearning import serviceLearning_bp

@serviceLearning_bp.route('/slcQuestionnaire')
def slcQuestionnaire():
    """This page requires faculties to answering questions regarding service learning proposal"""

    return render_template('serviceLearning/slcQuestionnaire.html')

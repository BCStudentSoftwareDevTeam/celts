from flask import request, render_template, g, abort
from app.controllers.serviceLearning import serviceLearning_bp


@serviceLearning_bp.route('/slcGuidelines')
def slcGuidelines():
    """This page display guildlines for creating service learning proposals"""

    return render_template('serviceLearning/slcGuidelines.html')

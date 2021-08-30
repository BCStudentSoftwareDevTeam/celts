from flask import request, render_template, g, abort
from app.controllers.serviceLearning import serviceLearning_bp


@serviceLearning_bp.route('/serviceCourseManagement', methods = ['GET'])
def serviceCourseManagement():
    """This is a Temporary Page for the Service Course Managment Screen."""
    print("Landed!!")

    return render_template('serviceLearning/serviceCourseManagment.html', title="Welcome to CELTS!")

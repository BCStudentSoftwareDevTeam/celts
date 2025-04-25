from flask import render_template, g, abort, request
from app.controllers.admin import admin_bp

from app.logic.bonner import getBonnerCohorts
from app.logic.graduationManagement import setGraduatedStatus, getGraduationManagementUsers


@admin_bp.route('/admin/graduationManagement', methods=['GET'])
def graduationManagement():
    if not g.current_user.isAdmin:
        abort(403)

    users = getGraduationManagementUsers()

    return render_template('/admin/graduationManagement.html', 
                           users = users,
                           cohortYears = getBonnerCohorts().keys())


@admin_bp.route('/<username>/setGraduationStatus/', methods=['POST'])
def setGraduationStatus(username):
    """
    This function 
    username: unique value of a user to correctly identify them
    """
    if not g.current_user.isAdmin:
        abort(403)
        
    status = request.form["status"]
    setGraduatedStatus(username, status)
    
    return ""

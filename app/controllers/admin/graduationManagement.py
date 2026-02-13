from flask import render_template, g, abort, request
from app.controllers.admin import admin_bp

from app.logic.bonner import getBonnerCohorts
from app.logic.graduationManagement import setGraduatedStatus, getGraduationManagementUsers, updateHideGraduatedStudents


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
    if not g.current_user.isAdmin:
        abort(403)
        
    status = request.form["status"]
    setGraduatedStatus(username, status)
    
    return ""

@admin_bp.route("/admin/hideGraduatedStudents/<username>", methods=["POST"])
def hideGraduatedStudents(username):
    if g.current_user.isStudent:
        abort(403) 
    
    checked = request.form["checked"]
    updateHideGraduatedStudents(username, checked)

    return ""

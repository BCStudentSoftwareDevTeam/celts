from flask import render_template, g, abort, request, redirect, url_for, flash, send_file
from app.models.user import User
from app.controllers.admin import admin_bp
from app.models.bonnerCohort import BonnerCohort

from app.logic.bonner import getBonnerCohorts
from app.logic.graduationManagement import setGraduatedStatus, makeGraduatedXls, getGraduationManagementUsers
from app.logic.minor import getMinorProgress


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
        
    try:
        status = request.form["status"]
        setGraduatedStatus(username, status)

    except Exception as e:
        print(e)
    
    return ""


@admin_bp.route("/gradStudentsxls/<filterType>", methods=['GET'])
def gradsXls(filterType):
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newfile = makeGraduatedXls(filterType)
    return send_file(open(newfile, 'rb'), download_name='GraduatedStudents.xlsx', as_attachment=True)


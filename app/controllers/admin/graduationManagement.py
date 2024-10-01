from flask import render_template, g, abort, request, redirect, url_for, flash
from app.models.user import User
from app.controllers.admin import admin_bp
from app.logic.bonner import getBonnerCohorts
from app.models.bonnerCohort import BonnerCohort

from app.logic.graduationManagement import getGraduatedStudent, removeGraduatedStudent


@admin_bp.route('/admin/graduationManagement', methods=['GET'])
def gradManagement():

    if not g.current_user.isAdmin:
        abort(403)

    users = User.select(User.username, User.hasGraduated, User.classLevel, User.firstName, User.lastName).where(User.classLevel=='Senior')

    bonnercohorts = getBonnerCohorts()
    
    return render_template('/admin/graduationManagement.html', users = users, 
                           bonnercohorts = bonnercohorts)


@admin_bp.route('/<username>/hasGraduated/', methods=['POST'])
def hasGraduated(username):
    """
    This function 
    username: unique value of a user to correctly identify them
    """
    try:
        success = getGraduatedStudent(username)
        if success:
            return "", 200
        else:
            return "", 500

    except Exception as e:
        print(e)
        return "Error Updating Graduation Status", 500

@admin_bp.route('/<username>/hasNotGraduated/', methods=['POST'])
def hasNotGraduated(username):
    """
    This function removes 
    username: unique value of a user to correctly identify them
    """
    try:
        removed = removeGraduatedStudent(username)
        if removed:
            flash("Graduation status has been updated!", "success")
            return "", 200
        else:
            flash("Error!", "Failed to update graduation status.")
            return "", 500
    except Exception as e:
        print(e)
        return "Error Updating Graduation Status", 500



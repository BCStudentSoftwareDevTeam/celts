from flask import Flask, render_template,request, flash, g, abort
import re
from app.controllers.admin import admin_bp
from app.models.user import User
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff

@admin_bp.route('/manageUsers', methods = ['POST'])
def manageUsers():
    eventData = request.form
    user = eventData['user']
    method = eventData['method']
    username = re.sub("[()]","", (user.split())[-1])
    user = User.get_by_id(username)

    if method == "addCeltsAdmin":
        addCeltsAdmin(user)
        flash(username+ " has been added as a Celts Admin", 'success')
    elif method == "addCeltsStudentStaff":
        addCeltsStudentStaff(user)
        flash(username+ " has been added as a Celts Student Staff", 'success')
    elif method == "removeCeltsAdmin":
        removeCeltsAdmin(user)
        flash(username+ " is no longer a Celts Admin ", 'success')
    elif method == "removeCeltsStudentStaff":
        removeCeltsStudentStaff(user)
        flash(username+ " is no longer a Celts Student Staff", 'success')

    return ("success")

@admin_bp.route('/userManagement', methods = ['GET'])
def userManagement():
    if g.current_user.isAdmin:
        return render_template('admin/userManagement.html')
    abort(403)

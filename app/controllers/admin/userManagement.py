from flask import Flask, render_template,request
from app.models.user import User
from app.controllers.admin import admin_bp
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff
import re

@admin_bp.route('/manageUsers', methods = ['POST'])
def manageUsers():
    eventData = request.form
    user = eventData['user']
    method = eventData['method']
    username = re.sub("[()]","", (user.split())[-1])
    user = User.get_by_id(username)

    if method == "addCeltsAdmin":
        addCeltsAdmin(user)
    elif method == "addCeltsStudentStaff":
        addCeltsStudentStaff(user)
    elif method == "removeCeltsAdmin":
        removeCeltsAdmin(user)
    elif method == "removeCeltsStudentStaff":
        removeCeltsStudentStaff(user)
    else:
        return {
        "There is an error":"error"
        }
    return ("success")

@admin_bp.route('/userManagement', methods = ['GET'])
def userManagement():
    return render_template('admin/userManagement.html')

from flask import Flask, render_template,request
from app.models.user import User
from app.controllers.admin import admin_bp
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff

@admin_bp.route('/manageUsers', methods = ['POST'])
def manageUsers():
    eventData = request.form
    print("event Data.......................",eventData)
    user = eventData.user
    method = eventData.method
    # we will give each method a number
    # method1 = addCeltsAdmin, 2 = addCeltsStudentStaff, 3= removeCeltsAdmin, 4 = removeCeltsStudentStaff
    print("..............................................The user is",user,"and the mrthod is",method)
    user = User.get_by_id(user)
    method = int(method)
    if method == 1:
        addCeltsAdmin(user)
    elif method == 2:
        addCeltsStudentStaff(user)
    elif method == 3:
        removeCeltsAdmin(user)
    elif method == 4:
        removeCeltsStudentStaff(user)
    else:
        return {
        "There is an error":"error"
        }
    return {"data":"1"}

@admin_bp.route('/userManagement', methods = ['GET'])
def userManagement():
    return render_template('admin/userManagement.html')

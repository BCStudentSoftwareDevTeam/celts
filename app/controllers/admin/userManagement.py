from flask import Flask, render_template,request, flash, g, abort, redirect, url_for
import re
from app.controllers.admin import admin_bp
from app.models.user import User
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff, addProgramManager, removeProgramManager
from app.logic.userManagement import changeCurrentTerm
from app.logic.utils import selectSurroundingTerms
from app.models.term import Term

@admin_bp.route('/admin/manageUsers', methods = ['POST'])
def manageUsers():
    eventData = request.form
    user = eventData['user']
    method = eventData['method']
    username = re.sub("[()]","", (user.split())[-1])
    user = User.get_by_id(username)

    if method == "addCeltsAdmin":
        if user.isCeltsAdmin:
            flash(username+ " is already a Celts Admin", 'danger')
        else:
            addCeltsAdmin(user)
            flash(username+ " has been added as a Celts Admin", 'success')
    elif method == "addCeltsStudentStaff":
        if user.isCeltsStudentStaff:
            flash(username+ " is already a Celts Student Staff", 'danger')
        else:
            addCeltsStudentStaff(user)
            flash(username+ " has been added as a Celts Student Staff", 'success')
    elif method == "removeCeltsAdmin":
        if not user.isCeltsAdmin:
            flash(username+ " is not a Celts Admin ", 'danger')
        else:
            removeCeltsAdmin(user)
            flash(username+ " is no longer a Celts Admin ", 'success')
    elif method == "removeCeltsStudentStaff":
        if not user.isCeltsStudentStaff:
            flash(username+ " is not a Celts Student Staff ", 'danger')
        else:
            removeCeltsStudentStaff(user)
            flash(username+ " is no longer a Celts Student Staff", 'success')
    return ("success")

@admin_bp.route('/updateManagers', methods=['POST','GET'])
def updateProgramManagers():
    eventData = request.form
    if eventData['status'] == "true":
        addProgramManager(eventData['user'],int(eventData['programID']))
    else:
        removeProgramManager(eventData['user'],int(eventData['programID']))
    return ""

@admin_bp.route('/admin', methods = ['GET'])
def userManagement():
    terms = selectSurroundingTerms(g.current_term)
    if g.current_user.isAdmin:
        return render_template('admin/userManagement.html',
                                terms=terms)
    abort(403)

@admin_bp.route('/admin/changeTerm', methods=['POST'])
def changeTerm():
    try:
        termData = request.form
        term = int(termData["id"])
        changeCurrentTerm(term)
        flash('Current term changed successfully', 'success')
    except:
        flash('Error. Current term request unsuccessful', 'warning')

    return ""

from flask import Flask, render_template,request, flash, g, json, abort, redirect, url_for
import re
from app.controllers.admin import admin_bp
from app.models.user import User
from app.models.program import Program
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff, addProgramManager, removeProgramManager
from app.logic.userManagement import changeCurrentTerm
from app.logic.userManagement import changeProgramInfo
from app.logic.utils import selectSurroundingTerms
from app.logic.userManagement import addNextTerm
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
            flash(user.firstName + " "+ user.lastName + " has been added as a Celts Admin", 'success')
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

@admin_bp.route('/addProgramManagers', methods=['POST'])
def addProgramManagers():

    eventData = request.form
    try:
        return addProgramManager(eventData['username'],int(eventData['programID']))
    except Exception as e:
        print(e)
        flash('Error while trying to add a manager.','warning')
        abort(500,"'Error while trying to add a manager.'")

@admin_bp.route('/removeProgramManagers', methods=['POST'])
def removeProgramManagers():

    eventData = request.form
    try:
        return removeProgramManager(eventData['username'],int(eventData['programID']))
    except Exception as e:
        print(e)
        flash('Error while removing a manager.','warning')
        abort(500,"Error while trying to remove a manager.")

@admin_bp.route('/admin/updateProgramInfo', methods=['POST'])
def updateProgramInfo():
    """Grabs info and then outputs it to logic function"""
    programInfo = request.form #grabs user inputs
    if g.current_user.isCeltsAdmin:
        try:
            return changeProgramInfo(programInfo["replyToEmail"],  #calls logic function to add data to database
                                    programInfo["senderName"],
                                    programInfo["programId"])
        except Exception as e:
            print(e)
            flash('Error while updating program info.','warning')
            abort(500,'Error while updating program.')
    abort(403)

@admin_bp.route('/admin', methods = ['GET'])
def userManagement():
    terms = selectSurroundingTerms(g.current_term)
    current_programs = Program.select()
    if g.current_user.isCeltsAdmin:
        return render_template('admin/userManagement.html',
                                terms=terms,
                                programs=list(current_programs))
    abort(403)

@admin_bp.route('/admin/changeTerm', methods=['POST'])
def changeTerm():
    try:
        termData = request.form
        term = int(termData["id"])
        changeCurrentTerm(term)
        flash(f'Current term successfully changed to {g.current_term.description}.', 'success')
    except:
        flash('Current term was not changed. Please try again.', 'warning')
    return ""

@admin_bp.route('/admin/addNewTerm', methods = ['POST'])
def addNewTerm():
    addNextTerm()
    return ""

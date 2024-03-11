from flask import render_template,request, flash, g, abort, redirect, url_for
import re
from app.controllers.admin import admin_bp
from app.models.user import User
from app.models.program import Program
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,addCeltsStudentAdmin ,removeCeltsAdmin,removeCeltsStudentStaff, removeCeltsStudentAdmin
from app.logic.userManagement import changeProgramInfo
from app.logic.utils import selectSurroundingTerms
from app.logic.term import addNextTerm, changeCurrentTerm

@admin_bp.route('/admin/manageUsers', methods = ['POST'])
def manageUsers():
    eventData = request.form
    user = eventData['user']
    method = eventData['method']
    username = re.sub("[()]","", (user.split())[-1])

    try:
        user = User.get_by_id(username)
    except Exception as e:
        print(e)
        flash(username + " is an invalid user.", "danger")
        return ("danger", 500)

    if method == "addCeltsAdmin":
        if user.isCeltsAdmin:
            flash(f"{user.fullName} is already a CELTS-Link Admin.", 'danger')
        elif user.isStudent and not user.isCeltsStudentStaff: 
            flash(f"{user.fullName} cannot be added as a CELTS-Link Admin.", 'danger')
        else: 
            addCeltsAdmin(user)
            flash(f"{user.fullName} has been added as a CELTS-Link Admin.", 'success')
    elif method == "addCeltsStudentStaff":
        if user.isCeltsStudentStaff:
            flash(f"{user.fullName} is already a CELTS Student Staff.", 'danger')
        elif user.isStudent:
            addCeltsStudentStaff(user)
            flash(f"{user.fullName} has been added as a CELTS Student Staff.", 'success')
        else:
            flash(username + " cannot be added as CELTS Student Staff.", 'danger')
    elif method == "addCeltsStudentAdmin":
        if user.isCeltsStudentAdmin:
            flash(f"{user.fullName} is already a CELTS Student Admin.", 'danger')
        elif user.isStudent: 
            addCeltsStudentAdmin(user)
            flash(f"{user.fullName} has been added as a CELTS Student Admin.", 'success')
        else: 
            flash(username + " cannot be added as CELTS Student Admin.", 'danger')
            
    elif method == "removeCeltsAdmin":
        removeCeltsAdmin(user)
        flash(f"{user.fullName} is no longer a CELTS Admin.", 'success')
    elif method == "removeCeltsStudentStaff":
        removeCeltsStudentStaff(user)
        flash(f"{user.fullName} is no longer a CELTS Student Staff.", 'success')
    elif method == "removeCeltsStudentAdmin":
        removeCeltsStudentAdmin(user)
        flash(f"{user.fullName} is no longer a CELTS Student Admin.", 'success')
    return ("success")

@admin_bp.route('/admin/updateProgramInfo/<programID>', methods=['POST'])
def updateProgramInfo(programID):
    """Grabs info and then outputs it to logic function"""
    programInfo = request.form # grabs user inputs
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentAdmin:
        try:
            changeProgramInfo(programInfo["programName"],  #calls logic function to add data to database
                              programInfo["contactEmail"],
                              programInfo["contactName"],
                              programInfo["location"],
                              programID)

            flash("Program updated", "success")
            return redirect(url_for("admin.userManagement", accordion="program"))
        except Exception as e:
            print(e)
            flash('Error while updating program info.','warning')
            abort(500,'Error while updating program.')
    abort(403)

@admin_bp.route('/admin', methods = ['GET'])
def userManagement():
    terms = selectSurroundingTerms(g.current_term)
    current_programs = Program.select()
    currentAdmins = list(User.select().where(User.isCeltsAdmin))
    currentStudentStaff = list(User.select().where(User.isCeltsStudentStaff))
    currentStudentAdmin = list(User.select().where(User.isCeltsStudentAdmin))
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentAdmin:
        return render_template('admin/userManagement.html',
                                terms = terms,
                                programs = list(current_programs),
                                currentAdmins = currentAdmins,
                                currentStudentStaff = currentStudentStaff,
                                currentStudentAdmin = currentStudentAdmin,
                                )
    abort(403)

@admin_bp.route('/admin/changeTerm', methods=['POST'])
def changeTerm():
    termData = request.form
    term = int(termData["id"])
    changeCurrentTerm(term)
    return ""

@admin_bp.route('/admin/addNewTerm', methods = ['POST'])
def addNewTerm():
    addNextTerm()
    return ""

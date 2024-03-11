from flask import render_template,request, flash, g, abort, redirect, url_for
import re
from typing import Dict, Any, List
from app.controllers.admin import admin_bp
from app.models.user import User
from app.models.program import Program
from app.models.term import Term
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,addCeltsStudentAdmin ,removeCeltsAdmin,removeCeltsStudentStaff, removeCeltsStudentAdmin
from app.logic.userManagement import changeProgramInfo
from app.logic.utils import selectSurroundingTerms
from app.logic.term import addNextTerm, changeCurrentTerm

@admin_bp.route('/admin/manageUsers', methods = ['POST'])
def manageUsers() -> str:
    eventData: Dict[str, str] = request.form
    user: str = eventData['user']
    method: str = eventData['method']
    username: str = re.sub("[()]","", (user.split())[-1])

    try:
        user: User = User.get_by_id(username)
    except Exception as e:
        print(e)
        flash(username + " is an invalid user.", "danger")
        return ("danger", 500)

    if method == "addCeltsAdmin":
        try:
            addCeltsAdmin(user)
            flash(f"{user.fullName} has been added as CELTS Admin.", 'success')
        except Exception as errorMessage:
            flash(str(errorMessage), 'danger')
        
    elif method == "addCeltsStudentStaff":
        try:
            addCeltsStudentStaff(user)
            flash(f"{user.fullName} has been added as CELTS Student Staff.", 'success')
        except Exception as errorMessage:
            flash(str(errorMessage), "danger")

    elif method == "addCeltsStudentAdmin":
        try:
            addCeltsStudentAdmin(user)
            flash(f"{user.fullName} has been added as CELTS Student Admin.", 'success')
        except Exception as errorMessage:
            flash(str(errorMessage), "danger")
            
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
def updateProgramInfo(programID: int) -> Any:
    """Grabs info and then outputs it to logic function"""
    programInfo: Dict[str, str] = request.form # grabs user inputs
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
def userManagement() -> str:
    terms: List[Term] = selectSurroundingTerms(g.current_term)
    currentPrograms: List[Program] = list(Program.select())
    currentAdmins: List[User] = list(User.select().where(User.isCeltsAdmin))
    currentStudentStaff: List[User] = list(User.select().where(User.isCeltsStudentStaff))
    currentStudentAdmin: List[User] = list(User.select().where(User.isCeltsStudentAdmin))
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentAdmin:
        return render_template('admin/userManagement.html',
                                terms = terms,
                                programs = currentPrograms,
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

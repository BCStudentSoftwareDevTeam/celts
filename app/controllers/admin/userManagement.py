from flask import render_template,request, flash, g, abort, redirect, url_for
import re
from app.controllers.admin import admin_bp
from app.models.user import User
from app.models.program import Program
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff
from app.logic.userManagement import changeProgramInfo
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.term import addNextTerm, changeCurrentTerm
from app.logic.fileHandler import FileHandler
from app.models.attachmentUpload import AttachmentUpload

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
        if user.isStudent and not user.isCeltsStudentStaff: 
            flash(user.firstName + " " + user.lastName + " cannot be added as a CELTS-Link admin", 'danger')
        else:
            if user.isCeltsAdmin:
                flash(user.firstName + " " + user.lastName + " is already a CELTS-Link Admin", 'danger')
            else: 
                addCeltsAdmin(user)
                flash(user.firstName + " " + user.lastName + " has been added as a CELTS-Link Admin", 'success')
    elif method == "addCeltsStudentStaff":
        if not user.isStudent:
            flash(username + " cannot be added as CELTS Student Staff", 'danger')
        else:
            if user.isCeltsStudentStaff:
                flash(user.firstName + " " + user.lastName + " is already a CELTS Student Staff", 'danger')
            else:
                addCeltsStudentStaff(user)
                flash(user.firstName + " " + user.lastName + " has been added as a CELTS Student Staff", 'success')
    elif method == "removeCeltsAdmin":
        removeCeltsAdmin(user)
        flash(user.firstName + " " + user.lastName + " is no longer a CELTS Admin ", 'success')
    elif method == "removeCeltsStudentStaff":
        removeCeltsStudentStaff(user)
        flash(user.firstName + " " + user.lastName + " is no longer a CELTS Student Staff", 'success')
    return ("success")

@admin_bp.route('/addProgramManagers', methods=['POST'])
def addProgramManagers():
    eventData = request.form
    try:
        return addProgramManagers(eventData['username'],int(eventData['programID']))
    except Exception as e:
        print(e)
        flash('Error while trying to add a manager.','warning')
        abort(500,"'Error while trying to add a manager.'")



@admin_bp.route('/deleteProgramFile', methods=['POST'])
def deleteProgramFile():
    programFile=FileHandler(programId=request.form["programID"])
    programFile.deleteFile(request.form["fileId"])
    return ""

@admin_bp.route('/admin/updateProgramInfo/<programID>', methods=['POST'])
def updateProgramInfo(programID):
    if g.current_user.isCeltsAdmin:
        try:
            programInfo = request.form # grabs user inputs
            uploadedFile = request.files.get('modalProgramImage')
            changeProgramInfo(programID, uploadedFile, **programInfo) 

            associatedAttachments = list(AttachmentUpload.select().where(AttachmentUpload.program == programID).execute()) 
           
            filePaths = FileHandler(programId=programID).retrievePath(associatedAttachments) 
          
            file_paths = {filename: path_info[0] for filename, path_info in filePaths.items()} 
            flash("Program updated", "success")
            return redirect(url_for("admin.userManagement", accordion="program"))
        except Exception as e:
            print("error: ", e)
            flash('Error while updating program info.','warning') 
            abort(500,'Error while updating program.')
    abort(403)

@admin_bp.route('/admin', methods = ['GET'])
def userManagement():
    terms = selectSurroundingTerms(g.current_term)
    current_programs = Program.select()
    currentAdmins = list(User.select().where(User.isCeltsAdmin))
    currentStudentStaff = list(User.select().where(User.isCeltsStudentStaff))
    if g.current_user.isCeltsAdmin:
        return render_template('admin/userManagement.html',
                                terms = terms,
                                programs = list(current_programs),
                                currentAdmins = currentAdmins,
                                currentStudentStaff = currentStudentStaff,
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

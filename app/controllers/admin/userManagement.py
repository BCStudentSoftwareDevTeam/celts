import os
from pathlib import Path

from app.models.term import Term
from flask import render_template,request, flash, g, abort, redirect, url_for, jsonify, session
from playhouse.shortcuts import model_to_dict
from peewee import fn, JOIN, DoesNotExist
import re
from werkzeug.utils import secure_filename


from app.controllers.admin import admin_bp
from app.models.user import User
from app.models.program import Program
from app.logic.fileHandler import FileHandler
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,removeCeltsAdmin,removeCeltsStudentStaff
from app.logic.userManagement import changeProgramInfo
from app.logic.participants import getTrainingsForInterestedParticipants, getParticipantsForProgramForAY
from app.logic.utils import selectSurroundingTerms
from app.logic.term import addNextTerm, changeCurrentTerm
from app.logic.users import getProgramInterest
from app.logic.volunteers import setProgramManager
from app.models.attachmentUpload import AttachmentUpload
from app.models.programManager import ProgramManager
from app.models.programBan import ProgramBan
from app.models.user import User

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


@admin_bp.route('/deleteProgramFile', methods=['POST'])
def deleteProgramFile():
    programFile=FileHandler(programId=request.form["programID"])
    programFile.deleteFile(request.form["fileId"])
    return ""

@admin_bp.route('/admin/updateProgramInfo/<programID>', methods=['POST'])
def updateProgramInfo(programID):
    if g.current_user.isCeltsAdmin or g.current_user.isProgramManagerFor(programID):
        try:
            programInfo = request.form # grabs user inputs
            uploadedFile = request.files.get('modalProgramImage')
            changeProgramInfo(programID, uploadedFile, **programInfo) 

            flash("Program updated", "success")
            return redirect(url_for("admin.userManagement", accordion="program"))
        except Exception as e:
            flash('Error while updating program info.','warning') 
            abort(500,'Error while updating program.')
    abort(403)


@admin_bp.route('/admin/getProgramInfo/<programID>', methods = ['GET'])
def getProgramInfo(programID):
    if g.current_user.isCeltsAdmin or g.current_user.isProgramManagerFor(programID):
        try:
            targetProgram = Program.get_by_id(programID)
            programInfo = model_to_dict(targetProgram, recurse=False)
            return jsonify([programInfo])
        except DoesNotExist as e:
            flash('Program not found')
            print("Debug Here \n", e)
            abort(404)
        except Exception as e:
            flash('Failed to retrieve data','warning') 
            print(e)
            abort(500, 'Failed to retrieve data')
    abort(403)


@admin_bp.route('/admin', methods = ['GET'])
def userManagement():
    terms = selectSurroundingTerms(g.current_term)

    currentPrograms = (
            Program
            .select(
                Program,
                fn.GROUP_CONCAT(fn.COALESCE(fn.CONCAT(User.firstName, ' ', User.lastName, '#', User.username), '')).alias('managers')
            )
            .join(ProgramManager, JOIN.LEFT_OUTER, on=(Program.id == ProgramManager.program))
            .join(User, JOIN.LEFT_OUTER, on=(ProgramManager.user == User.username))
    )

    if not g.current_user.isCeltsAdmin:
        currentPrograms = currentPrograms.where(ProgramManager.user == g.current_user.username)

    currentPrograms = currentPrograms.group_by(Program.id)
    
    currentAdmins = list(User.select().where(User.isCeltsAdmin))
    currentStudentStaff = list(User.select().where(User.isCeltsStudentStaff))
    currentTerm = Term.get(Term.isCurrentTerm)
    if g.current_user.isCeltsAdmin or g.current_user.isProgramManager:
        return render_template('admin/userManagement.html',
                                terms = terms,
                                programs = list(currentPrograms),
                                currentAdmins = currentAdmins,
                                currentStudentStaff = currentStudentStaff,
                                currentTerm = currentTerm
                                )
    abort(403)

@admin_bp.route('/admin/changeTerm', methods=['POST'])
def changeTerm():
    termData = request.form
    term = int(termData["id"])
    newTerm = changeCurrentTerm(term)
    return model_to_dict(newTerm)

@admin_bp.route('/admin/addNewTerm', methods = ['POST'])
def addNewTerm():
    addNextTerm()
    flash("New term added", "success")
    return ""

@admin_bp.route('/upload/<fileCategory>/<currentTerm>', methods = ['POST'])
def upload(fileCategory, currentTerm):
    term = Term.select().where(Term.id == currentTerm).get()
    allAYterm = Term.select().where(Term.academicYear == term.academicYear)
    if not fileCategory in ["laborHandbook", "volunteerHandbook", "backgroundForm"]:
        abort(405)
    dir_path = Path("app/static/files/", fileCategory)
    dir_path.mkdir(parents=True, exist_ok=True)
    file = request.files[fileCategory]
    filename = g.current_term.academicYear + "-" + fileCategory + "." + secure_filename(file.filename).split(".")[-1]
    full_path = os.path.join(dir_path, filename)
    if os.path.exists(full_path):
        os.remove(full_path)
    file.save(full_path)
    for t in allAYterm:
        if fileCategory == "volunteerHandbook":
            t.volunteerHandbook = filename
        elif fileCategory == "laborHandbook":
            t.laborHandbook = filename
        elif fileCategory == "backgroundForm":
            t.backgroundForm = filename
        else:
            abort(405)
        t.save()
    g.current_term = term
    flash(f"Handbook saved successfully to {term.description}!", "success")
    return redirect(request.referrer)

@admin_bp.route('/viewRoster/<programID>', methods = ['GET'])
def viewRoster(programID):
    program = Program.get_by_id(programID)
    interestedUsers = list(getProgramInterest(program)) 
    trainedAndInterested = getTrainingsForInterestedParticipants(programID, interestedUsers)

    lastAY = f"{int(g.current_term.academicYear.split("-")[0])-1}-{int(g.current_term.academicYear.split("-")[1])-1}"
    lastYearsParticipants = getParticipantsForProgramForAY(programID, lastAY)
    currentYearsParticipants = getParticipantsForProgramForAY(programID, g.current_term.academicYear)
    return render_template('admin/viewRoster.html',
                           program = program,
                           interestedUsers = interestedUsers, 
                           trainedAndInterested = trainedAndInterested,
                           lastYearsParticipants = lastYearsParticipants,
                           currentYearsParticipants = currentYearsParticipants,
                           lastAY = lastAY
                                )


import os
from pathlib import Path
import re

from flask import render_template,request, flash, g, abort, redirect, send_file, url_for, jsonify, session
from peewee import fn, JOIN, DoesNotExist
from playhouse.shortcuts import model_to_dict
from werkzeug.utils import secure_filename


from app import app
from app.logic.term import changeCurrentTerm
from app.controllers.admin import admin_bp
from app.logic.fileHandler import FileHandler
from app.logic.userManagement import addCeltsAdmin,addCeltsStudentStaff,createSpreadsheetForRosters,addCeltsOperationsTeam,removeCeltsAdmin,removeCeltsStudentStaff,removeCeltsOperationsTeam
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
from app.models.term import Term
from app.models.user import User
from app.models.program import Program

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
    elif method == "addCeltsOperationsTeam":
        if not user.isCeltsStudentStaff:
            flash(username + " cannot be added as CELTS Operations Team", "danger")
        else:
            if user.isCeltsOperationsTeam:
                flash(user.firstName + " " + user.lastName +" is already a CELTS Operations Team member", "danger")
            else:
                addCeltsOperationsTeam(user)
                flash(user.firstName + " " + user.lastName + " has been added as a CELTS Operations Team member", "success")
    elif method == "removeCeltsAdmin":
        removeCeltsAdmin(user)
        flash(user.firstName + " " + user.lastName + " is no longer a CELTS Admin ", 'success')
    elif method == "removeCeltsStudentStaff":
        removeCeltsStudentStaff(user)
        flash(user.firstName + " " + user.lastName + " is no longer a CELTS Student Staff", 'success')
    elif method == "removeCeltsOperationsTeam":
        if not user.isCeltsOperationsTeam:
            flash(user.firstName + " " + user.lastName +" is not a CELTS Operations Team member", "danger")
        else:
            removeCeltsOperationsTeam(user)
            flash(user.firstName + " " + user.lastName + " is no longer a CELTS Operations Team member", "success")    
    return ("success", 200)

@admin_bp.route('/deleteProgramFile', methods=['POST'])
def deleteProgramFile():
    programFile=FileHandler(programId=request.form["programID"])
    programFile.deleteFile(request.form["fileId"])
    return ""

@admin_bp.route('/admin/updateProgramInfo/<programID>', methods=['POST'])
def updateProgramInfo(programID):
    if g.current_user.isCeltsAdmin or g.current_user.isProgramManagerFor(programID) or g.current_user.isCeltsOperationsTeam:
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
    if g.current_user.isCeltsAdmin or g.current_user.isProgramManagerFor(programID) or g.current_user.isCeltsOperationsTeam:
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

    if not g.current_user.isCeltsAdmin and not g.current_user.isCeltsOperationsTeam: #Allows CELTS Operations Team to view all programs.
        currentPrograms = currentPrograms.where(ProgramManager.user == g.current_user.username)

    currentPrograms = list(currentPrograms.group_by(Program.id))
    currentAdmins = list(User.select().where(User.isCeltsAdmin))
    currentStudentStaff = list(User.select().where(User.isCeltsStudentStaff))
    if g.current_user.isCeltsAdmin or g.current_user.isProgramManager or g.current_user.isCeltsOperationsTeam:
        return render_template('admin/userManagement.html',
                                terms = terms,
                                programs = currentPrograms,
                                currentAdmins = currentAdmins,
                                currentStudentStaff = currentStudentStaff,
                                )
    abort(403)

@admin_bp.route('/admin/changeTerm', methods=['POST'])
def changeTerm():
    newTerm = changeCurrentTerm(int(request.form.get('id')))
    flash(f"Current term successfully changed to {newTerm.description}", "success")

    return ""

@admin_bp.route('/admin/addNewTerm', methods = ['POST'])
def addNewTerm():
    newTerm = addNextTerm()
    flash(f"Successfully added {newTerm.description}", "success")

    return ""

@admin_bp.route('/upload/<userFileCategory>/<userTermId>', methods = ['POST'])
def upload(userFileCategory, userTermId):
    try:
        handbookTerm = Term.get_by_id(userTermId)
    except DoesNotExist:
        abort(405)

    if userFileCategory not in ["laborHandbook", "volunteerHandbook"]:
        abort(405)
    fileCategory = userFileCategory

    # Save file to fs
    file = request.files[fileCategory]
    newFilename = g.current_term.academicYear + "-" + fileCategory + "." + secure_filename(file.filename).split(".")[-1]

    dir_path = Path(app.config['files']['base_path'], fileCategory)
    dir_path.mkdir(parents=True, exist_ok=True)
    full_path = os.path.join(dir_path, newFilename)
    if os.path.exists(full_path):
        os.remove(full_path)
    file.save(full_path)

    # Update all terms in the Academic Year with the handbook filename
    for ayTerm in Term.select().where(Term.academicYear == handbookTerm.academicYear):
        setattr(ayTerm, fileCategory, newFilename)
        ayTerm.save()

    # refresh the session with the new object
    changeCurrentTerm(g.current_term, refreshOnly=True)

    flash(f"Handbook saved successfully to {ayTerm.description}!", "success")
    return redirect(request.referrer)

@admin_bp.route('/viewRoster/<programID>', methods = ['GET'])
def viewRoster(programID):
    program = Program.get_by_id(programID)

    interestedUsers = list(getProgramInterest(program)) 
    trainedAndInterested = getTrainingsForInterestedParticipants(program, interestedUsers)
    lastYearsParticipants = getParticipantsForProgramForAY(program, g.current_term.previousAcademicYear)
    currentYearsParticipants = getParticipantsForProgramForAY(program, g.current_term.academicYear)
    return render_template('admin/viewRoster.html',
                           program = program,
                           interestedUsers = interestedUsers, 
                           trainedAndInterested = trainedAndInterested,
                           lastYearsParticipants = lastYearsParticipants,
                           currentYearsParticipants = currentYearsParticipants
                                )

@admin_bp.route('/exportRosters/<programID>/<academicYear>', methods = ['GET'])
def exportRosters(programID, academicYear):
    try:
        outFile = createSpreadsheetForRosters(academicYear, programID)
        filepath = os.path.abspath(outFile)
        return send_file(filepath, as_attachment=True, download_name=filepath.split("/")[-1], mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except DoesNotExist:
        abort(403)

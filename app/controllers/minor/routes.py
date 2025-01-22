from flask import g, render_template, request, abort, flash, redirect, url_for, jsonify
from peewee import DoesNotExist

from app.controllers.minor import minor_bp
from app.models.user import User
from app.models.term import Term
from app.models.summerExperience import SummerExperience
from app.models.otherExperience import OtherExperience

from app.logic.fileHandler import FileHandler
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.minor import saveOtherEngagementRequest, setCommunityEngagementForUser, getSummerTerms, getSummerExperience, getEngagementTotal, createSummerExperience, updateSummerExperience, getProgramEngagementHistory, getCourseInformation, getCommunityEngagementByTerm
import logging

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin):
        return abort(403)

    sustainedEngagementByTerm = getCommunityEngagementByTerm(username)
    selectedSummerTerm, summerExperience = getSummerExperience(username)

    summerYears = [2021, 2022, 2023, 2024, 2025]

    return render_template("minor/profile.html",
                            user = User.get_by_id(username),
                            summerYears = summerYears, 
                            sustainedEngagementByTerm = sustainedEngagementByTerm,
                            summerExperience = summerExperience if summerExperience else "",
                            selectedSummerTerm = selectedSummerTerm,
                            totalSustainedEngagements = getEngagementTotal(sustainedEngagementByTerm),
                            summerTerms = getSummerTerms(),
                            allTerms = getSummerExperience(username))

    
# ################################################## SUMMER EXPERIENCE START ###########################################################

@minor_bp.route('/cceMinor/<username>/addSummerExperience', methods=['POST'])
@minor_bp.route('/cceMinor/<username>/updateSummerExperience', methods=['GET', 'POST'])
def createOrUpdateSummerExperience(username):
    formData = request.form
    if request.path == f'/cceMinor/<username>/updateSummerExperience':
        try: 
            updateSummerExperience(username, formData)
            flash(f'Summer Experience successfully updated by {username}', 'success')
        except Exception as e:
            flash(f'An error occurred while adding the summer experience: {e}', 'danger')
            logging.error(f'An error occurred while adding the summer experience: {e}')
        return ""
    
    else:
        try: 
            createSummerExperience(username, formData)
            flash(f'Summer Experience successfully created by {username}', 'success')
        except Exception as e:
            flash(f'An error occurred while adding the summer experience: {e}', 'danger')
            logging.error(f'An error occurred while adding the summer experience: {e}')
        return redirect(url_for('minor.viewCceMinor', username=username)) 

# ################################################## SUMMER EXPERIENCE END ###########################################################

@minor_bp.route('/cceMinor/<username>/getEngagementInformation/<type>/<term>/<id>', methods=['GET'])
def getEngagementInformation(username, type, id, term):
    """
        For a particular engagement activity (program or course), get the participation history or course information respectively.
    """
    if type == "program":
        information = getProgramEngagementHistory(id, username, term)
    else:
        information = getCourseInformation(id)

    return information

@minor_bp.route('/cceMinor/<username>/modifyCommunityEngagement', methods=['PUT','DELETE'])
def modifyCommunityEngagement(username):
    """
        Saving a term participation/activities for sustained community engagement
    """
    if not g.current_user.isCeltsAdmin:
        abort(403)

    action = 'add' if request.method == 'PUT' else 'remove'
    try: 
        setCommunityEngagementForUser(action, request.form, g.current_user)
    except DoesNotExist:
        return "There are already 4 Sustained Community Engagement records." 
    
    return ""

@minor_bp.route('/cceMinor/<username>/requestOtherCommunityEngagement', methods=['GET', 'POST'])
def requestOtherEngagement(username):
    """
        Load the "request other" form and submit it.
    """
    user = User.get_by_id(username)
    terms = selectSurroundingTerms(g.current_term)
    

    if request.method == 'POST':
        filename = None
        attachment = request.files.get("attachmentObject")
        if attachment:
                addFile = FileHandler(getFilesFromRequest(request))
                addFile.saveFiles()
                filename = attachment.filename
        formData = request.form.copy()
        formData["filename"] = filename
        saveOtherEngagementRequest(formData)
        flash("Other community engagement request submitted.", "success")
        return redirect(url_for("minor.viewCceMinor", username=user))


    return render_template("/minor/requestOtherEngagement.html",
                            user=user,
                            terms=terms)

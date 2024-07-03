from flask import g, render_template, request, abort, flash, redirect, url_for
from peewee import DoesNotExist

from app.controllers.minor import minor_bp
from app.models.summerExperience import SummerExperience
from app.models.user import User
from app.logic.summerExperienceUtils import saveSummerExperience
from app.models.term import Term
from app.models.attachmentUpload import AttachmentUpload

from app.logic.fileHandler import FileHandler
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.minor import getProgramEngagementHistory, getCourseInformation, getCommunityEngagementByTerm, removeSummerExperience
from app.logic.minor import saveOtherEngagementRequest, setCommunityEngagementForUser, saveSummerExperience, getSummerTerms, getSummerExperience, getEngagementTotal


# ##################################################################################
# /profile/<username>/cceMinor
@minor_bp.route('/profile/<username>/cceMinorr', methods=['POST', 'GET']) 
def addSummerExperience(username):
    user = User.get(User.username == username)
    summer_experience_data = {
        'user': user,
        'fullName': request.form['fullName'],
        'email': request.form['studentEmail'],
        # All other fields from the form
        'roleDescription': request.form['roleDescription'],
        'experienceType': request.form['experienceType'],
        'contentArea': request.form.getlist('contentArea'),
        'experienceHoursOver300': request.form['experienceHoursOver300'] == 'Yes',
        'experienceHoursBelow300': request.form['experienceHoursBelow300'],
        'dateCreated': request.form['dateCreated'],
        'company': request.form['company'],
        'companyAddress': request.form['companyAddress'],
        'companyPhone': request.form['companyPhone'],
        'companyWebsite': request.form['companyWebsite'],
        'supervisorPhone': request.form['supervisorPhone'],
        'supervisorEmail': request.form['supervisorEmail'],
        'totalHours': request.form['totalHours'],
        'weeks': request.form['weeks'],
        'description': request.form['description'],
        'filename': request.form['filename'],
        'status': 'Pending'  # or however you want to set the initial status
    }
    print("test", summer_experience_data)
    
    saveSummerExperience(summer_experience_data)

    return render_template("minor/profile.html")
    
    # return redirect(url_for('minor_bp.viewCceMinor', username=username))


def addSummerExperience(username):
    saveSummerExperience(username, request.form, g.current_user)

    return ""
#######################################################################################

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin):
        return abort(403)

    sustainedEngagementByTerm = getCommunityEngagementByTerm(username)
    selectedSummerTerm, summerExperience = getSummerExperience(username)

    terms = selectSurroundingTerms(g.current_term)
    return render_template("minor/profile.html",
                            user = User.get_by_id(username),
                            sustainedEngagementByTerm = sustainedEngagementByTerm,
                            summerExperience = summerExperience if summerExperience else "",
                            selectedSummerTerm = selectedSummerTerm,
                            totalSustainedEngagements = getEngagementTotal(sustainedEngagementByTerm),
                            summerTerms = getSummerTerms(), terms=terms) 

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


@minor_bp.route('/cceMinor/<username>/deleteSummerExperience', methods=['POST'])
def deleteSummerExperience(username):        
    removeSummerExperience(username)

    return ""

from flask import g, render_template, request, abort, flash, redirect, url_for
from peewee import DoesNotExist

from app.controllers.minor import minor_bp
from app.models.user import User
from app.models.cceMinorProposal import CCEMinorProposal
from app.models.term import Term
from app.logic.fileHandler import FileHandler
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.minor import createOtherEngagementRequest, updateOtherEngagementRequest, setCommunityEngagementForUser, getSummerExperience, getEngagementTotal, createSummerExperience, updateSummerExperience, getProgramEngagementHistory, getCourseInformation, getCommunityEngagementByTerm, getCCEMinorProposals

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin):
        return abort(403)

    sustainedEngagementByTerm = getCommunityEngagementByTerm(username)

    return render_template("minor/profile.html",
                            user = User.get_by_id(username),
                            proposalList = getCCEMinorProposals(username),
                            sustainedEngagementByTerm = sustainedEngagementByTerm,
                            totalSustainedEngagements = getEngagementTotal(sustainedEngagementByTerm),
                            allTerms = getSummerExperience(username))
    
@minor_bp.route('/cceMinor/<username>/otherEngagement', methods=['GET', 'POST'])
def requestOtherEngagement(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin or g.current_user.username == username):
        return abort(403)

    # once we submit the form for creation
    if request.method == "POST":
        createOtherEngagementRequest(username, request.form)
        return redirect(url_for('minor.viewCceMinor', username=username))
    
    return render_template("minor/requestOtherEngagement.html",
                            editable = True,
                            user = User.get_by_id(username),
                            selectableTerms = selectSurroundingTerms(g.current_term),
                            otherEngagement = None)

@minor_bp.route('/cceMinor/editOtherEngagement/<proposalID>', methods=['GET', 'POST'])
@minor_bp.route('/cceMinor/viewOtherEngagement/<proposalID>', methods=['GET'])
@minor_bp.route('/cceMinor/viewSummerExperience/<proposalID>', methods=['GET'])
@minor_bp.route('/cceMinor/editSummerExperience/<proposalID>', methods=['GET', 'POST'])
def editOrViewProposal(proposalID: int):
    proposal = CCEMinorProposal.get_by_id(int(proposalID))
    if not (g.current_user.isAdmin or g.current_user.username == proposal.student):
        return abort(403)
    
    if request.method == "GET" and 'view' in request.path:
        return render_template("minor/requestOtherEngagement.html" if 'OtherEngagement' in request.path else "minor/requestSummerExperience.html",
                                editable = False,
                                user = User.get_by_id(proposal.student),
                                proposal = proposal)
    
    if request.method == "POST":
        if "OtherEngagement" in request.path:
            updateOtherEngagementRequest(proposalID, request.form)
        else:
            updateSummerExperience(proposalID, request.form)
 
        return redirect(url_for('minor.viewCceMinor', username=proposal.student))
    
    return render_template("minor/requestOtherEngagement.html" if 'OtherEngagement' in request.path else "minor/requestSummerExperience.html",
                            editable = True,
                            selectableTerms = selectSurroundingTerms(g.current_term, summerOnly=False if 'OtherEngagement' else True),
                            user = User.get_by_id(proposal.student),
                            proposal = proposal)

@minor_bp.route('/cceMinor/<username>/summerExperience', methods=['GET', 'POST'])
def requestSummerExperience(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin or g.current_user.username == username):
        return abort(403)
    
    # once we submit the form for creation
    if request.method == "POST":
        createSummerExperience(username, request.form)
        return redirect(url_for('minor.viewCceMinor', username=username))
    
    summerTerms = selectSurroundingTerms(g.current_term, summerOnly=True)

    return render_template("minor/summerExperience.html",
                            selectableTerms = summerTerms,
                            user = User.get_by_id(username),
                            )

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


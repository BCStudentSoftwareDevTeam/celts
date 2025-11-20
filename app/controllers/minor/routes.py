from flask import g, render_template, request, abort, flash, redirect, url_for
from peewee import DoesNotExist

from app.controllers.minor import minor_bp
from app.models.user import User
from app.models.cceMinorProposal import CCEMinorProposal
from app.models.term import Term
from app.models.attachmentUpload import AttachmentUpload
from app.logic.fileHandler import FileHandler
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.minor import (
    changeProposalStatus,
    createOtherEngagement,
    updateOtherEngagementRequest,
    setCommunityEngagementForUser,
    getEngagementTotal,
    createSummerExperience,
    updateSummerExperience,
    getProgramEngagementHistory, 
    getCourseInformation,
    getCommunityEngagementByTerm,
    getMinorSpreadsheet,
    getCCEMinorProposals,
    removeProposal
)

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """

    sustainedEngagementByTerm = getCommunityEngagementByTerm(username)

    activeTab = request.args.get("tab", "sustainedCommunityEngagements")

    return render_template("minor/profile.html",
                            user = User.get_by_id(username),
                            proposalList = getCCEMinorProposals(username),
                            sustainedEngagementByTerm = sustainedEngagementByTerm,
                            totalSustainedEngagements = getEngagementTotal(sustainedEngagementByTerm),
                            activeTab=activeTab)
    
@minor_bp.route('/cceMinor/<username>/otherEngagement', methods=['GET', 'POST'])
def createOtherEngagementRequest(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin or g.current_user.username == username):
        return abort(403)
    

    # once we submit the form for creation
    if request.method == "POST":
        createOtherEngagement(username, request)

        return redirect(url_for('minor.viewCceMinor', username=username))
    
    return render_template("minor/requestOtherEngagement.html",
                            editable = True,
                            user = User.get_by_id(username),
                            selectableTerms = selectSurroundingTerms(g.current_term),
                            postRoute = f"/cceMinor/{username}/otherEngagement", # when form is submitted, what POST route is it being submitted to.
                            attachmentFilePath = "",
                            attachmentFileName = "",
                            proposal = None)

@minor_bp.route('/cceMinor/viewOtherEngagement/<proposalID>', methods=['GET'])
@minor_bp.route('/cceMinor/viewSummerExperience/<proposalID>', methods=['GET'])
@minor_bp.route('/cceMinor/editOtherEngagement/<proposalID>', methods=['GET', 'POST'])
@minor_bp.route('/cceMinor/editSummerExperience/<proposalID>', methods=['GET', 'POST'])
def editOrViewProposal(proposalID: int):
    proposal = CCEMinorProposal.get_by_id(int(proposalID))
    if not (g.current_user.isAdmin or g.current_user.username == proposal.student.username):
        return abort(403)
    
    editProposal = 'view' not in request.path

    # if proposal is approved, only admins can edit, but not if the admin is the student
    if proposal.isApproved and editProposal:
        if g.current_user.username == proposal.student or not g.current_user.isAdmin:
            return abort(403)
    
    attachmentObject = AttachmentUpload.get_or_none(proposal=proposalID)
    attachmentFilePath = ""
    attachmentFileName = ""

    if attachmentObject:
        fileHandler = FileHandler(proposalId=proposalID)
        attachmentFilePath = fileHandler.getFileFullPath(attachmentObject.fileName).lstrip("app/") # we need to remove app/ from the url because it prevents it from displaying
        attachmentFileName = attachmentObject.fileName
    
    if request.method == "GET":
        selectedTerm = Term.get_by_id(proposal.term)
        flash("Once approved, a proposal can only be edited by an admin.", 'warning')
        return render_template("minor/requestOtherEngagement.html" if 'OtherEngagement' in request.path else "minor/summerExperience.html",
                                editable = editProposal,
                                selectedTerm = selectedTerm,
                                contentAreas = proposal.contentAreas.split(", ") if proposal.contentAreas else [],
                                selectableTerms = selectSurroundingTerms(g.current_term, summerOnly=False if 'OtherEngagement' else True),
                                user = User.get_by_id(proposal.student),
                                postRoute = f"/cceMinor/editSummerExperience/{proposal.id}" if "SummerExperience" in request.path else f"/cceMinor/editOtherEngagement/{proposal.id}",
                                proposal = proposal,
                                attachmentFilePath = attachmentFilePath,
                                attachmentFileName = attachmentFileName
        )
    
    if "OtherEngagement" in request.path:
        updateOtherEngagementRequest(proposalID, request)
    else:
        updateSummerExperience(proposalID, request.form)
 
    return redirect(url_for('minor.viewCceMinor', username=proposal.student))

@minor_bp.route('/cceMinor/<username>/summerExperience', methods=['GET', 'POST'])
def createSummerExperienceRequest(username):
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
                            contentAreas = [],
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


@minor_bp.route('/cceMinor/<action>/<username>/<proposalId>', methods=['POST'])
def updateProposal(action, username, proposalId):
    try:
        if not (g.current_user.isAdmin or g.current_user.isFaculty or g.current_user.username == username):
            flash("Unauthorized to perform this action", "warning")
            return ""

        actionMap = {
            "withdraw": ("Withdrawn", "Proposal successfully withdrawn"),
            "complete": ("Completed", "Proposal successfully completed"),
            "approve": ("Approved", "Proposal approved"),
            "unapprove": ("Submitted", "Proposal unapproved"),
        }

        if action not in actionMap:
            flash("Invalid action", "warning")
            return ""

        newStatus, message = actionMap[action]
        changeProposalStatus(proposalId, newStatus)
        flash(message, "success")

    except Exception as e:
        print(e)
        flash("Proposal status could not be changed", "warning")

    return ""


@minor_bp.route('/cceMinor/getMinorSpreadsheet', methods=['GET'])
def returnMinorSpreadsheet():
    """
        Returns a spreadsheet containing users and related spreadsheet information.
    """
    minorSpreadsheet = getMinorSpreadsheet()   # can we get for any term or only curr term?

    return minorSpreadsheet

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


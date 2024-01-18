from flask import Flask, g, render_template, request, abort, flash, redirect, url_for
from app.controllers.minor import minor_bp
from app.models.user import User
from app.models.term import Term
from app.logic.utils import selectSurroundingTerms
from app.logic.fileHandler import FileHandler
from app.models.attachmentUpload import AttachmentUpload
from app.logic.utils import getFilesFromRequest
from app.logic.minor import toggleMinorInterest, getProgramEngagementHistory, getCourseInformation, getCommunityEngagementByTerm, saveOtherEngagementRequest

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin):
        return abort(403)
    terms = getCommunityEngagementByTerm(username)
    user = User.get_by_id(username)
    return render_template("minor/profile.html",
                    user=user,
                    terms=terms)

@minor_bp.route('/cceMinor/<username>/identifyCommunityEngagement/<term>', methods=['GET'])
def identifyCommunityEngagement(username):
    """
        Load all program and course participation records for that term
    """
    pass

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

@minor_bp.route('/cceMinor/<username>/addCommunityEngagement', methods=['POST'])
def addCommunityEngagement(username):
    """
        Saving a term participation/activities for sustained community engagement
    """
    pass

@minor_bp.route('/cceMinor/<username>/removeCommunityEngagement', methods=['POST'])
def removeCommunityEngagement(username):
    """
        Opposite of above
    """
    pass

@minor_bp.route('/cceMinor/<username>/requestOtherCommunityEngagement', methods=['GET', 'POST'])
def requestOtherEngagement(username):
    """
        Load the "request other" form and submit it.
    """
    user = User.get_by_id(username)
    terms = selectSurroundingTerms(g.current_term)
    

    if request.method == 'POST':
        flash("Something happened and we hit post", "success")
        attachmentName = None
        attachment = request.files.get("attachmentObject")
        if attachment:
                addFile= FileHandler(getFilesFromRequest(request))
                addFile.saveFiles()
                attachmentName = attachment.filename
        formData = request.form.copy()
        formData["attachment"] = attachmentName
        saveOtherEngagementRequest(formData)
        return redirect(url_for("minor.viewCceMinor", username=user))


    return render_template("/minor/requestOtherEngagement.html",
                            user=user,
                            terms=terms)



@minor_bp.route('/cceMinor/<username>/addSummerExperience', methods=['POST'])
def addSummerExperience(username):
    pass

@minor_bp.route('/cceMinor/<username>/indicateInterest', methods=['POST'])
def indicateMinorInterest(username):
    toggleMinorInterest(username)

    return ""

@minor_bp.route("/deleteRequestFile", methods=["POST"])
def deleteRequestFile():

    fileData= request.form
    termFile=FileHandler(termId=fileData["databaseId"])
    termFile.deleteFile(fileData["fileId"])

    return ""

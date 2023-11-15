from flask import Flask, g, render_template, request
from app.controllers.minor import minor_bp
from app.models.user import User

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """
    pass

@minor_bp.route('/cceMinor/<username>/identifyCommunityEngagement/<term>', methods=['GET'])
def identifyCommunityEngagement(username):
    """
        Load all program and course participation records for that term
    """
    pass

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

@minor_bp.route('/cceMinor/<username>/requestOtherCommunityEngagement', methods=['GET'])
def requestOtherEngagement(username):
    """
        Load the "request other" form and submit it.
    """
    user = User.get_by_id(username)

    return render_template("/minor/requestOtherEngagement.html",
                            user=user)



@minor_bp.route('/cceMinor/<username>/addSummerExperience', methods=['POST'])
def addSummerExperience(username):
    pass

@minor_bp.route('/cceMinor/<username>/indicateInterest', methods=['POST'])
def indicateMinorInterest(username):
    pass


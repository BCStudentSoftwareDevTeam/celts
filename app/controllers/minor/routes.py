from flask import Flask, g

from app.controllers.minor import minor_bp

@minor_bp.route('/profile/<username>/cceMinor', methods=[''])
def viewCceMinor():
    pass

@minor_bp.route('cceMinor/getTermActivities', methods=[''])
def getTermActivities():
    pass

@minor_bp.route('cceMinor/removeTermActivitie', methods=[''])
def removeTermActivitie():
    pass

@minor_bp.route('/cceMinor/getCommunityEngagements', methods=[''])
def getCommunityEngagements():
    pass

@minor_bp.route('/cceMinor/getEventsInProgram', methods=[''])
def getEventsInProgram():
    pass

@minor_bp.route('/cceMinor/addCommunityEngagement', methods=[''])
def addCommunityEngagement():
    pass

@minor_bp.route('/cceMinor/removeCommunityEngagement', methods=[''])
def removeCommunityEngagement():
    pass

@minor_bp.route('/cceMinor/addOtherCommunityEngagement', methods=[''])
def addOtherCommunityEngagement():
    pass

@minor_bp.route('/cceMinor/addSummerExperience', methods=[''])
def addSummerExperience():
    pass

@minor_bp.route('/profile/<username>/cceMinor/otherCommunityEngagement', methods=[''])
def requestOtherCommunityEngagement():
    pass

@minor_bp.route('/profile/<username>/cceMinor/addOtherCommunityEngagement', methods=[''])
def addOtherCommunityEngagement():
    pass

@minor_bp.route('cceMinor/requestOtherEngagement/addSupervisorVerification', methods=[''])
def addSupervisorVerification():
    pass

@minor_bp.route('/cceMinor/indicateInterest', methods=[''])
def indicateMinorInterest():
    pass

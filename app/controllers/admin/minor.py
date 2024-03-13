from flask import render_template, g, abort
import json

from app.controllers.admin import admin_bp
from app.logic.courseManagement import unapprovedCourses
from app.logic.minor import getMinorInterest, getMinorProgress


@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    if not g.current_user.isAdmin:
        abort(403)
    interestedStudents = getMinorInterest()
    sustainedEngagement = getMinorProgress()

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudents, 
                            sustainedEngagement = sustainedEngagement )

@admin_bp.route('/admin/getInterestedStudentsCount', methods=['GET'])
def getInterestedStudentsCount() -> str:
    """
    Get the count of students interested in the CCE minor to display in the 
    admin sidebar. It must be returned as a string to be received by the
    ajax request.
    """
    interestedStudentsCount: int = len(getMinorInterest())
    return str(interestedStudentsCount)



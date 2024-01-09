from flask import render_template, g, abort
from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest
from app.logic.minor import getMinorProgress


@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    if g.current_user.isAdmin:
        interestedStudents= getMinorInterest()
        sustainedEngagement = getMinorProgress()

        return render_template('/admin/cceMinor.html',
                               interestedStudentsList = interestedStudents, 
                               sustainedEngagement = sustainedEngagement )
    else: 
        abort(403)

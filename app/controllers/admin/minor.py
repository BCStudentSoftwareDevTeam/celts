from flask import render_template, g, abort

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress

@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    if not g.current_user.isAdmin:
        abort(403)

    interestedStudents = getMinorInterest()
    sustainedEngagement = getMinorProgress()

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudents, 
                            sustainedEngagement = sustainedEngagement,
                            )

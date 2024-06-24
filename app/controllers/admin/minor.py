from flask import render_template, g, abort

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress

@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    if not g.current_user.isAdmin:
        abort(403)
 
    interestedStudentsList = getMinorInterest()
    interestedStudentEmailString = ';'.join([student['email'] for student in interestedStudentsList])
    sustainedEngagement = getMinorProgress()

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            sustainedEngagement = sustainedEngagement,
                            )

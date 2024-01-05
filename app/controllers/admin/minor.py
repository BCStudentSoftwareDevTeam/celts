from flask import render_template, g, abort
from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest
from app.logic.minor import getEngagedStudentsWithRequirementCount


@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    if g.current_user.isAdmin:
        interestedStudents= getMinorInterest()
        engagedStudents = getEngagedStudentsWithRequirementCount()

        return render_template('/admin/cceMinor.html',
                               interestedStudentsList = interestedStudents, 
                               engagedStudentList = engagedStudents )
    else: 
        abort(403)

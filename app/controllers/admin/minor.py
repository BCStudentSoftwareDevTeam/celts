from flask import render_template
from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest
from app.logic.minor import getEngagedStudentsWithRequirementCount


@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    interestedStudents= getMinorInterest()
    engagedStudents = getEngagedStudentsWithRequirementCount()

    return render_template('/admin/cceMinor.html',interestedStudentsList = interestedStudents, engagedStudentList = engagedStudents )


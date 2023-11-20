from flask import render_template
from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest
from app.logic.minor import getEngagedStudents
from app.logic.minor import getRequirementCount



@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    interestedStudents= getMinorInterest()
    engagedStudents= getEngagedStudents()
    requirementCount = getRequirementCount()

    return render_template('/admin/cceMinor.html', interestedStudentsList=interestedStudents, engagedStudentList = engagedStudents)


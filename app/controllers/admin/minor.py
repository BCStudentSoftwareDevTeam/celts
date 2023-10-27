from flask import render_template
from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest


@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    interestedStudents= getMinorInterest()

    return render_template('/admin/cceMinor.html', studentList=interestedStudents)
from flask import render_template, g, abort, request, redirect, url_for
from app.models.user import User
from app.controllers.admin import admin_bp
from app.logic.graduationManagement import getGradutedStudents

@admin_bp.route('/admin/graduationManagement', methods=['POST','GET'])
def gradManagement():

    if not g.current_user.isAdmin:
        abort(403)
    
    graduatedStudents = getGradutedStudents()

    

    return render_template('/admin/graduationManagement.html',
                            graduatedStudents = graduatedStudents
                            )



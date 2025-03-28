from flask import render_template, g, abort, request, redirect, url_for, send_file

from app.models.user import User

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress, toggleMinorInterest, getMinorSpreadsheet

@admin_bp.route('/admin/cceMinor', methods=['POST','GET'])
def manageMinor():

    if not g.current_user.isAdmin:
        abort(403)
    
    if request.method == 'POST':
        interested_students = request.form.getlist('interestedStudents[]')

        for i in interested_students:
            user = User.get(username=i)
            if not user.minorInterest:
                toggleMinorInterest(i)    


    interestedStudentsList = getMinorInterest()
    interestedStudentEmailString = ';'.join([student['email'] for student in interestedStudentsList])
    sustainedEngagement = getMinorProgress()
    

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            sustainedEngagement = sustainedEngagement,
                            )

@admin_bp.route("/admin/cceMinor/download")
def downloadSpreadsheet():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newfile = getMinorSpreadsheet()
    return send_file(open(newfile, 'rb'), download_name='minor_progress.xlsx', as_attachment=True)



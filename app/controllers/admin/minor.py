from flask import render_template, g, abort, request, redirect, url_for, send_file, jsonify
from app.logic.minor import getMinorProgress
from app.models.user import User

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress, toggleMinorInterest, getMinorSpreadsheet, getDeclaredMinorStudents

@admin_bp.route('/profile/<username>/cceMinorChart', methods=['GET'])
def cceMinorChart(username):
    if not g.current_user.isAdmin:
        abort(403)
    else:
        progressList = getMinorProgress()
        turnToChart = []
        for progress in progressList:
            turnToChart.append({'name':progress["firstName"] + " " + progress["lastName"], "engagementCount" : progress['engagementCount'], "completeSummer": "Yes" if progress['hasSummer'] == "Complete" else "No"})
        return jsonify(turnToChart)
    
@admin_bp.route('/admin/cceMinor', methods=['GET','POST'])
def manageMinor():
    if not g.current_user.isAdmin:
        abort(403)
    
    if request.method == 'POST':
        interestedStudents = request.form.getlist('interestedStudents[]')
        for student in interestedStudents:
            user = User.get(username=student)
            if not user.minorInterest:
                toggleMinorInterest(student, True)  
                 
        return redirect(url_for("admin.manageMinor"))



    interestedStudentsList = getMinorInterest()
    interestedStudentEmailString = ';'.join([student['email'] for student in interestedStudentsList])
    sustainedEngagement = getMinorProgress()
    declaredStudentsList = getDeclaredMinorStudents()
    declaredStudentEmailString = ';'.join([student['email'] for student in declaredStudentsList])   
    adminUsername = g.current_user.username 

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudentsList,
                            declaredStudentsList = declaredStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            declaredStudentEmailString = declaredStudentEmailString,
                            sustainedEngagement = sustainedEngagement,
                            adminUsername = adminUsername,
                            )

@admin_bp.route("/admin/cceMinor/download")
def downloadSpreadsheet():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newfile = getMinorSpreadsheet()
    return send_file(open(newfile, 'rb'), download_name='minor_progress.xlsx', as_attachment=True)



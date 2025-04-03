from flask import render_template, g, abort, request, redirect, url_for

from app.models.user import User

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress, toggleMinorInterest, getDeclaredMinorStudents

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

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudentsList,
                            declaredStudentsList = declaredStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            declaredStudentEmailString = declaredStudentEmailString,
                            sustainedEngagement = sustainedEngagement,
                            )
    
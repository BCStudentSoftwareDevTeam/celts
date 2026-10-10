from flask import render_template, g, abort, request, redirect, url_for, send_file

from app.models.user import User

from app.controllers.admin import admin_bp

from app.logic.minor import getDeclaredMinorStudents, getMinorInterest, getMinorProgress, toggleMinorInterest, getMinorSpreadsheet

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
    declaredStudentsDict = getDeclaredMinorStudents()
    declaredStudentEmailString = ';'.join([student['email'] for student in declaredStudentsDict])  
          
    cceMinorStudents = declaredStudentsDict


    return render_template('/admin/cceMinor.html',
                            cceMinorStudents = cceMinorStudents,
                            interestedStudentsList = interestedStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            declaredStudentEmailString = declaredStudentEmailString,
                            )

@admin_bp.route("/admin/cceMinor/download")
def downloadSpreadsheet():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newfile = getMinorSpreadsheet()
    return send_file(open(newfile, 'rb'), download_name='minor_progress.xlsx', as_attachment=True)



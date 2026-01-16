from flask import render_template, g, abort, request, redirect, url_for, send_file

from app.models.user import User

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress, toggleMinorInterest, getMinorSpreadsheet, getDeclaredMinorStudents

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
    print(sustainedEngagement)
    declaredStudentsList = getDeclaredMinorStudents()
    print("These are the declaredStudents", declaredStudentsList)
    declaredStudentEmailString = ';'.join([student['email'] for student in declaredStudentsList])  
      
    declaredUsernames = {
        s['username']
        for s in declaredStudentsList
        if s.get('declaredMinor')
    }
    
    sustainedUsernames = {
        s['username']
        for s in sustainedEngagement
    }
    
    # merging both lists 
    cceMinorStudents = {}
    # if they are in sustainedEngagement and have been declared
    for student in sustainedEngagement:
        cceMinorStudents[student['username']] = {
            **student,
            'isDeclaredMinor': student['username'] in declaredUsernames
        }
        
    for student in declaredStudentsList:
        if student['username'] not in sustainedUsernames:
            cceMinorStudents[student['username']] = {
                **student,
                'engagementCount': 0, 
                'hasSummer': 'Incomplete',
                'hasCCEMinorProposal': False
            }
    cceMinorStudents = list(cceMinorStudents.values())


    return render_template('/admin/cceMinor.html',
                            cceMinorStudents = cceMinorStudents,
                            interestedStudentsList = interestedStudentsList,
                            declaredStudentsList = declaredStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            declaredStudentEmailString = declaredStudentEmailString,
                            sustainedEngagement = sustainedEngagement,
                            )

@admin_bp.route("/admin/cceMinor/download")
def downloadSpreadsheet():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    newfile = getMinorSpreadsheet()
    return send_file(open(newfile, 'rb'), download_name='minor_progress.xlsx', as_attachment=True)



from flask import render_template, g, abort, request, redirect, url_for

from app.controllers.admin import admin_bp

from app.logic.minor import getMinorInterest, getMinorProgress, toggleMinorInterest, checkToggle

@admin_bp.route('/admin/cceMinor', methods=['POST','GET'])
def manageMinor():

    if not g.current_user.isAdmin:
        abort(403)
    
    if request.method == 'POST':
        interested_students = request.form.getlist('interestedStudents[]')
        for i in interested_students:
            if checkToggle(i) == False:
                toggleMinorInterest(i)    


    interestedStudentsList = getMinorInterest()
    interestedStudentEmailString = ';'.join([student['email'] for student in interestedStudentsList])
    sustainedEngagement = getMinorProgress()
    

    return render_template('/admin/cceMinor.html',
                            interestedStudentsList = interestedStudentsList,
                            interestedStudentEmailString = interestedStudentEmailString,
                            sustainedEngagement = sustainedEngagement,
                            )

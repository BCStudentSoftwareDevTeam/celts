from app.controllers.admin import admin_bp

@admin_bp.route('/manageMinor', methods=[''])
def manageMinor():
    pass

@admin_bp.route('/manageMinor/currentStudents', methods=[''])
def getCurrentStudents():
    pass

@admin_bp.route('/manageMinor/interestedStudents', methods=[''])
def getInterestedStudents():
    pass
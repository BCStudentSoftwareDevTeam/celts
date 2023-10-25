from flask import render_template
from app.controllers.admin import admin_bp

@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
    user = User.get(User.username == username)
        return render_template('/admin/cceMinor.html',
                                user = user)
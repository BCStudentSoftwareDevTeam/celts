from flask import render_template
from app.controllers.admin import admin_bp

@admin_bp.route('/admin/cceMinor', methods=['GET'])
def manageMinor():
        return render_template('/admin/cceMinor.html')



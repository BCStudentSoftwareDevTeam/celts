from flask import render_template, g, abort, request, redirect, url_for
from app.models.user import User
from app.controllers.admin import admin_bp


@admin_bp.route('/admin/graduationManagement', methods=['GET'])
def gradManagement():

    if not g.current_user.isAdmin:
        abort(403)

    users = User.select(User.username, User.hasGraduated, User.classLevel)

    return render_template('/admin/graduationManagement.html', users = users)



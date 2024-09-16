from flask import render_template, g, abort, request, redirect, url_for
from app.models.user import User
from app.controllers.admin import admin_bp


@admin_bp.route('/admin/graduationManagement', methods=['GET', 'POST'])
def gradManagement():

    if not g.current_user.isAdmin:
        abort(403)

    users = User.select(User.username, User.hasGraduated, User.classLevel, User.firstName, User.lastName).where(User.classLevel=='Senior')

    if request.method == 'POST':
        username = request.form.get('username')
        has_graduated = request.form.get('hasGraduated') == 'true'

        # Find the user by username
        user = User.get_or_none(User.username == username)

        if user:
            # Update the graduation status
            user.hasGraduated = has_graduated
            user.save()
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404


    return render_template('/admin/graduationManagement.html', users = users)






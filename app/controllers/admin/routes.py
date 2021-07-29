from flask import request, render_template
from flask import Flask, redirect, flash, url_for, g, abort
from app.models.user import User
from app.controllers.admin import admin_bp, getStudent

@admin_bp.route('/testing', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    students = User.select()
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff:
        return render_template("/searchStudentPage.html", students = students)
    abort(403)

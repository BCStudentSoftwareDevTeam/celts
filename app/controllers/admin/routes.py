from flask import request, render_template
from flask import Flask, redirect, flash, url_for
from app.models.user import User
from app.controllers.admin import admin_bp, updateSearchStudent

@admin_bp.route('/testing', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    students = User.select()
    return render_template("/searchStudentPage.html", students = students)


@admin_bp.route('/volunteerProfile/<user>', methods=['POST'])
def volunteerProfile(user):
    # user = user.strip("()")
    # userName=user.split('(')[-1]
    # print(userName)
    return redirect(url_for('admin.testing'))

from flask import request, flash
from app.controllers.admin import admin_bp
from app.models.course import Course
from peewee import *

@admin_bp.route('/withdrawCourse/<course>', methods = ['POST'])
def withdrawCourse(course):
    (Course.delete().where(Course.courseName == course)).execute()
    flash("Course successfully withdrawn")
    return "Course successfully withdrawn"

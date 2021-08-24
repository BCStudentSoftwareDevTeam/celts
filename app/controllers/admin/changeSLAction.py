from flask import request, flash
from app.controllers.admin import admin_bp
from app.models.course import Course
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from peewee import *

@admin_bp.route('/withdrawCourse/<course>', methods = ['POST'])
def withdrawCourse(course):
    course = Course.get(Course.courseName == course)
    (CourseInstructor.delete().where(CourseInstructor.course == course)).execute()  #need to delete all ForeignKeyFields first
    (CourseParticipant.delete().where(CourseParticipant.course == course)).execute()
    course.delete_instance()
    flash("Course successfully withdrawn", success)
    return "Course successfully withdrawn"

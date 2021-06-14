from flask import request, render_template
from app.models.program import Program

from app.controllers.main import main_bp

@main_bp.route('/volunteerIndicateInterest', methods = ['GET'])
def volunteerIndicateInterest():
    programs = Program.select()
    return render_template('volunteerIndicateInterest.html',
                           title="Volunteer Interest",
                           programs = programs)

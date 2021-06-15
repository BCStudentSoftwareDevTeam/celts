from flask import request, render_template
from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest

from app.controllers.main import main_bp

@main_bp.route('/volunteerIndicateInterest', methods = ['GET'])
def volunteerIndicateInterest():
    programs = Program.select()
    return render_template('volunteerIndicateInterest.html',
                           title="Volunteer Interest",
                           programs = programs)


@main_bp.route('/updateInterest/<program_id>', methods = ['POST'])
def updateInterest(program_id, user_id):
    pass

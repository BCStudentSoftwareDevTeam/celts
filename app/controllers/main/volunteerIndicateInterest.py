from flask import request, render_template
from flask import json, jsonify
from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest

from app.controllers.main import main_bp

current_user = User.get(User.username == "escalerapadronl") #FIXME: Remove once authentication is built

@main_bp.route('/volunteerIndicateInterest', methods = ['GET'])
def volunteerIndicateInterest():
    programs = Program.select()
    return render_template('volunteerIndicateInterest.html',
                           title="Volunteer Interest",
                           programs = programs)


@main_bp.route('/updateInterest/<program_id>/<interest>', methods = ['POST'])
def updateInterest(program_id, interest):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program or by deleting the row from the table when a
    user no longer shows interest in a program.
    """
    if interest:
        Interest.create(program_id, current_user.username)
    else:
        deleted_interest = Interest.get(Interest.program == program_id and Interest.user == current_user.username)
        deleted_interest.delete_instance()
    return jsonify({"Success": False})

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


@main_bp.route('/updateInterest/<program_id>/<num_interest>', methods = ['POST'])
def updateInterest(program_id, num_interest):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program or by deleting the row from the table when a
    user no longer shows interest in a program.
    """
    print(type(num_interest))
    num_interest = int(num_interest)
    if num_interest:
        print("Stepped into if")
        Interest.get_or_create(program = program_id, user = current_user.username)
    else:
        print("stepped into else")
        deleted_interest = Interest.get(Interest.program == program_id and Interest.user == current_user.username)
        print(deleted_interest)
        deleted_interest.delete_instance()
    return jsonify({"Success": False})

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
    interests = Interest.select().where(Interest.user == current_user.username)
    return render_template('volunteerIndicateInterest.html',
                           title="Volunteer Interest",
                           user = current_user,
                           programs = programs,
                           interests = interests)


@main_bp.route('/updateInterest/<program_id>/<num_interest>', methods = ['POST'])
def updateInterest(program_id, num_interest):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program or by deleting the row from the table when a
    user no longer shows interest in a program.
    """
    num_interest = int(num_interest) #change this to a boolean
    try:
        if num_interest:
            Interest.get_or_create(program = program_id, user = current_user.username)
        else:
            deleted_interest = Interest.get(Interest.program == program_id and Interest.user == current_user.username) #change this to get_or_none
            deleted_interest.delete_instance()
        return jsonify({"Success": True}) #remove this
    except Exception as e:
        print("Error Updating Interest: ", e)
        return jsonify({"Success": False}),500


#add a route for delete interest

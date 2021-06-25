from flask import request, render_template
from flask import json, jsonify
from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest
from flask import g
from app.controllers.main import main_bp
from flask import request

@main_bp.route('/volunteerIndicateInterest', methods = ['GET'])

def volunteerIndicateInterest():
    programs = Program.select()
    interests = Interest.select().where(Interest.user_id == g.current_user)
    interests_ids = [interest.program_id for interest in interests]
    return render_template('volunteerIndicateInterest.html',
                           title="Volunteer Interest",
                           user = g.current_user,
                           programs = programs,
                           interests = interests,
                           interests_ids = interests_ids)

@main_bp.route('/deleteInterest/<program_id>', methods = ['POST'])
@main_bp.route('/addInterest/<program_id>', methods = ['POST'])
def updateInterest(program_id):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
    rule = request.url_rule
    try:
        if 'addInterest' in rule.rule:
            Interest.get_or_create(program = program_id, user = g.current_user)
        else:
            deleted_interest = Interest.get(Interest.program == program_id and Interest.user == g.current_user)
            deleted_interest.delete_instance()
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return "Error Updating Interest", 500

# @main_bp.route('/deleteInterest/<program_id>', methods = ['POST'])
# def deleteInterest(program_id):
#     """
#     This function updates the interest table by removing a row when the user
#     removes interest from a program
#     """
#     try:
#         deleted_interest = Interest.get(Interest.program == program_id and Interest.user == g.current_user)
#         deleted_interest.delete_instance()
#         return jsonify(success=True)
#     except Exception as e:
#         print(e)
#         return "Error Updating Interest", 500

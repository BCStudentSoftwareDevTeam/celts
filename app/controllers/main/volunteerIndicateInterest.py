from flask import request, render_template
from flask import json, jsonify
from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest
from flask import g
from app.controllers.main import main_bp
from flask import request
from app.logic.addRemoveInterest import addRemoveInterest

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
    user = g.current_user
    try:
        return addRemoveInterest(rule, program_id, user)

    except Exception as e:
        print(e)
        return "Error Updating Interest", 500

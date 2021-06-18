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


# @main_bp.route('/updateInterest/<program_id>/<num_interest>', methods = ['POST'])
# def updateInterest(program_id, num_interest):
#     """
#     This function updates the interest table by adding a new row when a user
#     shows interest in a program or by deleting the row from the table when a
#     user no longer shows interest in a program.
#     """
#     num_interest = int(num_interest) #change this to a boolean
#     try:
#         if num_interest:
#             Interest.get_or_create(program = program_id, user = current_user.username)
#         else:
#             deleted_interest = Interest.get(Interest.program == program_id and Interest.user == current_user.username) #change this to get_or_none
#             deleted_interest.delete_instance()
#         return jsonify({"Success": True}) #remove this
#     except Exception as e:
#         print("Error Updating Interest: ", e)
#         return jsonify({"Success": False}),500

@main_bp.route('/addInterest/<program_id>/<userID>', methods = ['POST'])
def addInterest(program_id, userID):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
    print(userID)
    print(program_id)
    try:
        Interest.create(program = program_id, user = current_user.username)
        return jsonify({"Success": True}) #remove this
    except Exception as e:
        print("Error Updating Interest: ", e)
        return jsonify({"Success": False}),500

@main_bp.route('/deleteInterest/<program_id>/<userID>', methods = ['POST'])
def deleteInterest(program_id, userID):
    """
    This function updates the interest table by removing a row when the user
    removes interest from a program
    """
    try:
        deleted_interest = Interest.get(Interest.program == program_id and Interest.user == current_user.username) #change this to get_or_none
        deleted_interest.delete_instance()
        return jsonify({"Success": True}) #remove this
    except Exception as e:
        print("Error Updating Interest: ", e)
        return jsonify({"Success": False}),500



#separate the update interest route into two:Addinterest and deleted_interest
#passing the programID and UserId from the html with the javascript
#first part of the conditional will be the Addinterestroute and second part will be delete interest route
#last part is conditional in the py file should in be javascript file

#add a route for delete interest

import pytest
from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest
from app.controllers.main import main_bp
from flask import g
from flask import jsonify


def addRemoveInterest(rule, program_id, currentUser):
    """
    This function is used to add or remove interest from the interest table.
    Parameters:
    rule: Gets the url from the ajax call, specifies to add or remove interest
    program_id: id of the program the user is interested in
    """
    print(rule)
    print(type(rule))
    #print(type(rule.rule))
    if 'addInterest' in str(rule):
        Interest.get_or_create(program = program_id, user = currentUser)
    else:
        deleted_interest = Interest.get(Interest.program == program_id, Interest.user == currentUser)
        print(deleted_interest)
        deleted_interest.delete_instance()
    return 'True'

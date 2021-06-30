from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest
from app.controllers.main import main_bp


def updateInterest(program_id):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
    rule = "addInterest"
    if 'addInterest' in rule:
        Interest.get_or_create(program = program_id, user = "ramasayb2")
    else:
        deleted_interest = Interest.get(Interest.program == program_id and Interest.user == "ramasayb2")
        deleted_interest.delete_instance()
